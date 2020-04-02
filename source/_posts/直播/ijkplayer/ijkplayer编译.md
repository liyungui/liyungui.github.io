---
title: ijkplayer编译
date: 2019-08-05 15:22:14
categories:
  - 直播
tags:
  - 直播
---

# install homebrew, git, yasm

```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install git
brew install yasm
```

# 配置sdk和ndk

- nkd只支持r11到r14。[ndk历史版本下载地址](https://developer.android.google.cn/ndk/downloads/)

```
# add these lines to your ~/.bash_profile or ~/.profile
vim ~/.bash_profile
# 添加 export ANDROID_SDK=<your sdk path>
# 添加 export ANDROID_NDK=<your ndk path>

# 使 ~/.bash_profile 生效
source ~/.bash_profile
```

## ndk版本检查

检查NDK版本，支持11 12 13 14版本，然而AS默认提供的NDK下载支持一般都比较新（18），不匹配报 `You need the NDKr10e or later`

 `ijkplayer/android/contrib/tools/do-detect-env.sh`

```
IJK_NDK_REL=$(grep -o '^Pkg\.Revision.*=[0-9]*.*' $ANDROID_NDK/source.properties 2>/dev/null | sed 's/[[:space:]]*//g' | cut -d "=" -f 2)
echo "IJK_NDK_REL=$IJK_NDK_REL"
case "$IJK_NDK_REL" in
    11*|12*|13*|14*)
        if test -d ${ANDROID_NDK}/toolchains/arm-linux-androideabi-4.9
        then
            echo "NDKr$IJK_NDK_REL detected"
        else
            echo "You need the NDKr10e or later"
            exit 1
        fi
    ;;
    *)
        echo "You need the NDKr10e or later"
        exit 1
    ;;
```    
# 克隆项目

`git clone https://github.com/Bilibili/ijkplayer.git ijkplayer-android`

# 下载并编译ffmpeg

- 需要翻墙

```
# 进入ijkplay-android目录
cd ijkplayer-android 

# 下载安装ffmpeg
# 此处需要翻墙，下载时长较长。下载目录位于extra
./init-android.sh

# 配置编译选项 
# 进入config文件夹
cd config
# 移除默认的配置
rm module.sh
#软链接module-default.sh为module.sh
ln -s module-default.sh module.sh

# 进入android/contrib目录
cd ..
cd android/contrib
# 清理ffmpeg的编译产物
./compile-ffmpeg.sh clean
# 编译ffmpeg的所有架构
./compile-ffmpeg.sh all
```

## 编译脚本支持参数

```
echo_usage() {
    echo "Usage:"
    echo "  compile-ffmpeg.sh armv5|armv7a|arm64|x86|x86_64"
    echo "  compile-ffmpeg.sh all|all32"
    echo "  compile-ffmpeg.sh all64"
    echo "  compile-ffmpeg.sh clean"
    echo "  compile-ffmpeg.sh check"
    exit 1
}
```

## 编译产物

编译成功 会在 `android/contrib` 相应模块生成 `libijkffmpeg.so`

比如 `android/contrib/build/ffmpeg-armv5/output/libijkffmpeg.so`

# 编译ijkplayer

```
# 进入android目录
cd ..
# 编译ijkplayer所有架构
./compile-ijk.sh all
```

## 编译脚本支持参数

```
echo "Usage:"
echo "  compile-ijk.sh armv5|armv7a|arm64|x86|x86_64"
echo "  compile-ijk.sh all|all32"
echo "  compile-ijk.sh all64"
echo "  compile-ijk.sh clean"
```
        
## 编译产物

编译成功 会在等相应模块生成三个so库

- `libijkffmpeg.so`
- `libijkplayer.so`
- `libijksdl.so`

比如 模块目录 `android/ijkplayer/ijkplayer-armv5/src/main/libs/armeabi-v7a`

# 参考&扩展

- [ijkplayer](https://github.com/bilibili/ijkplayer)