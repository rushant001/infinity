// Copyright(C) 2023 InfiniFlow, Inc. All rights reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

module;

import stl;

export module serialize;

namespace infinity {

//template <typename T>
//concept POD = IsTrivial<T> && IsStandLayout<T>;

export template <typename T>
inline i32 GetSizeInBytes(const T &) {
    static_assert(IsStandLayout<T>, "T must be POD");
    return sizeof(T);
}

export template <>
inline i32 GetSizeInBytes(const String &value) {
    return sizeof(i32) + value.length();
}

export template <typename T>
inline T ReadBuf(char *const buf) {
    static_assert(IsStandLayout<T>, "T must be POD");
    T *ptr = (T *)buf;
    T value = *ptr;
    return value;
}

export template <typename T>
inline T ReadBufAdv(char *&buf) {
    static_assert(IsStandLayout<T>, "T must be POD");
    T *ptr = (T *)buf;
    T value = *ptr;
    buf += sizeof(T);
    return value;
}

export template <>
inline String ReadBuf<String>(char *const buf) {
    i32 size = ReadBuf<i32>(buf);
    String str(buf + sizeof(i32), size);
    return str;
}

export template <>
inline String ReadBufAdv<String>(char *&buf) {
    i32 size = ReadBufAdv<i32>(buf);
    String str(buf, size);
    buf += size;
    return str;
}

export template <typename T>
inline void WriteBuf(char *const buf, const T &value) {
    static_assert(IsStandLayout<T>, "T must be POD");
    T *ptr = (T *)buf;
    *ptr = value;
}

export template <typename T>
inline void WriteBufAdv(char *&buf, const T &value) {
    static_assert(IsStandLayout<T>, "T must be POD");
    T *ptr = (T *)buf;
    *ptr = value;
    buf += sizeof(T);
}

export template <>
inline void WriteBuf<String>(char *const buf, const String &value) {
    i32 len = value.length();
    WriteBuf(buf, len);
    std::memcpy(buf + len, value.c_str(), len);
}

export template <>
inline void WriteBufAdv<String>(char *&buf, const String &value) {
    i32 len = value.length();
    WriteBufAdv(buf, len);
    std::memcpy(buf, value.c_str(), len);
    buf += len;
}

} // namespace infinity