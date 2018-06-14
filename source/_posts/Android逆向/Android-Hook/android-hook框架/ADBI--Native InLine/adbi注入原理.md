---
title: adbi 注入原理
date: 2018-05-18 16:44:42
tags: 
	- Hook

---

[Android平台下hook框架adbi的研究（上）](http://blog.csdn.net/roland_sun/article/details/34109569)

[adbi源代码](https://github.com/crmulliner/adbi)

Linux可以利用ptrace()函数来attach到一个进程上，从而可以修改对应该进程的内存内容和寄存器的值

adbi（The Android Dynamic Binary Instrumentation Toolkit）是一个通用的框架，使得hook变得异常简单。

# 进程注入基本实现原理 #

利用ptrace()attach到一个进程上，然后在进程调用序列中插入一个调用dlopen()加载so文件（初始化函数中hook指定的函数）的步骤。

adbi工具集由两个主要模块组成，分别是用于注入.so文件的进程劫持工具（hijack tool）和一个修改函数入口的基础库。

接下来，我们还是通过阅读代码来分别了解这两个模块的实现原理，本篇我们先将重点放在劫持工具的实现上。

**注入进程需要解决两个问题**

1. 获得目标进程dlopen()函数的调用地址
2. 插入一个调用dlopen()函数的步骤到目标进程的调用序列中。

## 1. 获得目标进程dlopen()函数的调用地址 ##
	----main()-----------------------------------------------------------------------
	//在当前进程中dlopen()加载libdl.so动态库，接着用dlsym()函数获得当前进程dlopen()函数的调用地址
	//libdl.so动态库肯定早已加载到当前进程中了，这里再加载一次并不会真的再在内存中的另一个位置加载一次，而是返回已经加载过的地址
	void *ldl = dlopen("libdl.so", RTLD_LAZY);  
	if (ldl) {  
	    dlopenaddr = dlsym(ldl, "dlopen");  
	    dlclose(ldl);  
	}  
	  
	unsigned long int lkaddr; //本进程linker地址。linker是Android提供的动态链接器，不同于普通的Linux。dlopen()函数就是在linker里面定义的（bionic/linker/dlfcn.cpp中: soinfo libdl_info = {"libdl.so"）  
	unsigned long int lkaddr2; //目标进程linker地址   
	find_linker(getpid(), &lkaddr);  
	find_linker(pid, &lkaddr2);  
	  
	dlopenaddr = lkaddr2 + (dlopenaddr - lkaddr); //同一台机器上的进程肯定用的是同一个linker，所以其内部的dlopen()函数和linker头的偏移量是固定的

	----find_linker()-----------------------------------------------------------------------
	static int find_linker(pid_t pid, unsigned long *addr) {  
	    struct mm mm[1000];  
	    unsigned long libcaddr;  
	    int nmm;  
	    char libc[256];  
	    symtab_t s;  
	  
	    if (0 > load_memmap(pid, mm, &nmm)) {  
	        printf("cannot read memory map\n");  
	        return -1;  
	    }  
	    if (0 > find_linker_mem(libc, sizeof(libc), &libcaddr, mm, nmm)) {  
	        printf("cannot find libc\n");  
	        return -1;  
	    }  
	      
	    *addr = libcaddr;  
	      
	    return 1;  
	} 

	  	----load_memmap()-----------------------------------------------------------------------
		static int load_memmap(pid_t pid, struct mm *mm, int *nmmp) {  
		    char raw[80000]; // this depends on the number of libraries an executable uses  
		    char name[MAX_NAME_LEN];  
		    char *p;  
		    unsigned long start, end;  
		    struct mm *m;  
		    int nmm = 0;  
		    int fd, rv;  
		    int i;  
		  
			//打开文件(路径是“/proc/<进程号>/maps”)读出指定进程的内存映射信息，其格式大概如下：
		    sprintf(raw, "/proc/%d/maps", pid);  
		    fd = open(raw, O_RDONLY);  
		    if (0 > fd) {  
		        printf("Can't open %s for reading\n", raw);  
		        return -1;  
		    }  

			//逐行读取内存映射信息文件的内容
			memset(raw, 0, sizeof(raw));  /* Zero to ensure data is null terminated */  			  
			p = raw;  
			while (1) {  
			    rv = read(fd, p, sizeof(raw)-(p-raw));  
			    if (0 > rv) {  
			        return -1;  
			    }  
			    if (0 == rv)  
			        break;  
			    p += rv;  
			    if (p-raw >= sizeof(raw)) {  
			        printf("Too many memory mapping\n");  
			        return -1;  
			    }  
			}  
			close(fd);  

			//逐行解析内存映射信息文件的内容。文件格式如下：
			40096000-40098000 r-xp 00000000 b3:16 109        /system/bin/app_process  
			40098000-40099000 r--p 00001000 b3:16 109        /system/bin/app_process  
			40099000-4009a000 rw-p 00000000 00:00 0   
			4009a000-400a9000 r-xp 00000000 b3:16 176        /system/bin/linker  
			400a9000-400aa000 r--p 0000e000 b3:16 176        /system/bin/linker  
			400aa000-400ab000 rw-p 0000f000 b3:16 176        /system/bin/linker  
			400ab000-400ae000 rw-p 00000000 00:00 0   
			400ae000-400b0000 r--p 00000000 00:00 0   
			400b0000-400b9000 r-xp 00000000 b3:16 855        /system/lib/libcutils.so  
			be846000-be867000 rw-p 00000000 00:00 0          [stack] 
		    p = strtok(raw, "\n");  
		    m = mm;  
		    while (p) {  
		        /* parse current map line */  
		        rv = sscanf(p, "%08lx-%08lx %*s %*s %*s %*s %s\n",  
		            &start, &end, name);  //解析出当前行的 起始地址，结束地址，和名称。
		  
		        p = strtok(NULL, "\n");  //获取下一行
		  
		        if (rv == 2) {  //没有解析出名称(只有两个返回值)，就会用一个自定义的名称补上（“[memory]”）
		            m = &mm[nmm++];  
		            m->start = start;  
		            m->end = end;  
		            strcpy(m->name, MEMORY_ONLY);  
		            continue;  
		        }  
		  
		        if (strstr(name, "stack") != 0) {  //名字是“stack”，表明这段内存用于栈
		            stack_start = start;  
		            stack_end = end;  
		        }  
		  		
				//将连续的并且名字相同的内存段合并一下.(从前面的格式中可以看出，会有几行都叫一个名字的情况)
		        /* search backward for other mapping with same name */  
		        for (i = nmm-1; i >= 0; i--) {  
		            m = &mm[i];  
		            if (!strcmp(m->name, name))  
		                break;  
		        }  
		  
		        if (i >= 0) {  
		            if (start < m->start)  
		                m->start = start;  
		            if (end > m->end)  
		                m->end = end;  
		        } else {  
		            /* new entry */  
		            m = &mm[nmm++];  
		            m->start = start;  
		            m->end = end;  
		            strcpy(m->name, name);  
		    }  
		  
		    *nmmp = nmm;  
		    return 0;  
		} 

		----find_linker_mem()-----------------------------------------------------------------------
		static int find_linker_mem(char *name, int len, unsigned long *start, struct mm *mm, int nmm) {  
		    int i;  
		    struct mm *m;  
		    char *p;  
		    for (i = 0, m = mm; i < nmm; i++, m++) {  
		        if (!strcmp(m->name, MEMORY_ONLY))  
		            continue;  
		        p = strrchr(m->name, '/');  
		        if (!p)  
		            continue;  
		        p++;  
		        if (strncmp("linker", p, 6))  //找出名字以“linker”结尾(/system/bin/linker)的那段内存的起始地址。
		            continue;  
		    break;  
		    }  
		    if (i >= nmm)  
		    /* not found */  
		        return -1;  
		  
		    *start = m->start;  
		    strncpy(name, m->name, len);  
		    if (strlen(m->name) >= len)  
		        name[len-1] = '\0';  
		    return 0;  
		}  

## 2. 插入一个调用dlopen()函数的步骤到目标进程的调用序列中 ##

	// Attach 
	if (0 > ptrace(PTRACE_ATTACH, pid, 0, 0)) {//被Attach的进程将成为当前进程的子进程，并且会暂停执行。
		printf("cannot attach to %d, error!\n", pid);
		exit(1);
	}
	waitpid(pid, NULL, 0);//等待被Attach的进程暂停运行才返回
	ptrace(PTRACE_GETREGS, pid, 0, &regs); //获得目标进程的所有寄存器的值
	//unsigned int sc[]
	sc[11] = regs.ARM_r0;  
	sc[12] = regs.ARM_r1;  
	sc[13] = regs.ARM_r2;  
	sc[14] = regs.ARM_r3;  
	sc[15] = regs.ARM_lr;  
	sc[16] = regs.ARM_pc;  
	sc[17] = regs.ARM_sp;  
	sc[19] = dlopenaddr;
	// push library name to stack  
	//case 'l': n = strlen(optarg)+1; n = n/4 + (n%4 ? 1 : 0); 
	//命令行-l参数后就是so库完整名称。ptrace()写入目标进程以4字节为单位 
	libaddr = regs.ARM_sp - n*4 - sizeof(sc);  
	sc[18] = libaddr; 
	// write library name to stack  
	if (0 > write_mem(pid, (unsigned long*)arg, n, libaddr)) {  
	    printf("cannot write library name (%s) to stack, error!\n", arg);  
	    exit(1);  
	}  
	// write code to stack  
	codeaddr = regs.ARM_sp - sizeof(sc);  
	if (0 > write_mem(pid, (unsigned long*)&sc, sizeof(sc)/sizeof(long), codeaddr)) {  
	    printf("cannot write code, error!\n");  
	    exit(1);  
	}

		----write_mem()-----------------------------------------------------------------------
		/* Write NLONG 4 byte words from BUF into PID starting at address POS.  Calling process must be attached to PID. */  
		static int write_mem(pid_t pid, unsigned long *buf, int nlong, unsigned long pos) {  
		    unsigned long *p;  
		    int i;  
		  
		    for (p = buf, i = 0; i < nlong; p++, i++)  
		        if (0 > ptrace(PTRACE_POKETEXT, pid, pos+(i*4), *p))  
		            return -1;  
		    return 0;  
		}

	mprotect()给栈内存段设置可执行属性。
		adbi采用了另一种方法找目标进程mprotect()内存地址。
		思路是分析ELF文件libc.so来获得其中符号mprotect的值（其实就是mprotect()函数相对于文件头的偏移），再加上libc.so文件在内存中映射的起始地址，就是mprotect()函数真正的调用地址了
	// calc stack pointer  
	regs.ARM_sp = regs.ARM_sp - n*4 - sizeof(sc);  
	  
	// call mprotect() to make stack executable  
	regs.ARM_r0 = stack_start; // want to make stack executable  
	regs.ARM_r1 = stack_end - stack_start; // stack size  
	regs.ARM_r2 = PROT_READ|PROT_WRITE|PROT_EXEC; // protections  
	  
	regs.ARM_lr = codeaddr; // points to loading and fixing code  
	regs.ARM_pc = mprotectaddr; // execute mprotect()

	ptrace(PTRACE_SETREGS, pid, 0, &regs);  
	ptrace(PTRACE_DETACH, pid, 0, SIGCONT); //deAttach,让目标进程恢复运行 
	
