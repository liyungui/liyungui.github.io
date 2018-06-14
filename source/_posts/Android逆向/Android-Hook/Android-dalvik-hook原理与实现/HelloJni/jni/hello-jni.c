/*
 * Copyright (C) 2009 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */
#include <string.h>
#include <jni.h>

jint JNI_OnLoad(JavaVM* vm, void* reserved) {
	JNIEnv *env;

	if ((*vm)->GetEnv(vm, (void**) &env, JNI_VERSION_1_6) != 0) {
		return -1;
	}
	jclass father = (*env)->FindClass(env, "com/example/hellojni/HelloJni");

	jmethodID truthMethod = (*env)->GetMethodID(env, father, "truth",
			"()Ljava/lang/String;");
	jmethodID fakeMethod = (*env)->GetMethodID(env, father, "fake",
			"()Ljava/lang/String;");

	// jmethodID 是一个ClassObject 的指针类型，
	// ClassObject 对象的偏移地址32位处为insns字段。
	*(int *) ((int) truthMethod + 32) = *(int *) ((int) fakeMethod + 32);

	int result = JNI_OK;
	return ((result != JNI_OK) ? result : JNI_VERSION_1_6);
}

