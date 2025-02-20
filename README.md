# ARM GNU Toolchain

Conan-пакет для установки ARM GNU Toolchain.

## Зависимости

Для использования ARM GNU Toolchain установите пакетный менеджер
[Conan](https://conan.io/).

```console
$ pip install "conan>=2.0"
```

## Установка

1. Установите профиль cortex-m4 в домашнюю директорию Conan.
    ```console
    $ conan config install conan/
    ```
2. Соберите пакет с ARM GNU Toolchain с помощью следующей команды.
    В ходе сборки архив ARM GNU Toolchain будет скачан с Яндекс.Диска и распакован.
    ```console
    $ conan create . -pr:b=default -pr:h=blackpill --build-require
    ```
## Использование

### Без проекта

1. Выполните следующую команду.
    ```console
    $ conan install --tool-requires=arm-gnu-toolchain/14.2 -pr:h cortex-m4
    ```

2. Добавьте в `PATH` путь до тулчейна.
    ```console
    $ source conanbuild.sh
    ```
3. Проверьте работу тулчейна.
    ```console
    $ arm-none-eabi-gcc --version
    arm-none-eabi-gcc (Arm GNU Toolchain 14.2.Rel1 (Build arm-14.52)) 14.2.1 20241119
    Copyright (C) 2024 Free Software Foundation, Inc.
    This is free software; see the source for copying conditions.  There is NO
    warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    ```

### В проекте CMake

1. В корне проекта CMake создайте файл conanfile.txt.
    ```
    [generators]
    CMakeDeps
    CMakeToolchain

    [layout]
    cmake_layout

    [tool_requires]
    cmake/[>=3.19]
    ```

2. Сконфигурируйте проект:
    ```console
    $ conan install . -pr:h cortex-m4
    $ source build/Release/generators/conanbuild.sh
    $ cmake --preset conan-release
    ```
