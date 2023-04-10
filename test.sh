#!/bin/bash

function module_exist {
    if [ -f "./test/$1_test.py" ]; then
        return 0
    fi
    return 1
}

function test_module {
    py="$1"
    module="$2"
    path=`command -v $py`
    if [ -x "$path" ]; then
        echo "using $path"
        if module_exist $module; then
            echo "Testing $2"
            eval "$path -m test.$2_test "
        else
            eval "$path -m test.run"
        fi
    else
        echo "$py 不可执行"
    fi
}


function test {
    py_exe="$1"
    module="$2"
    if [ -n "$py_exe" ]; then
        test_module $py_exe $module

    else
        echo "自动测试"
        if [ -x "`command -v python`" ]; then
            python2 --version
            command python2 -m test.run
            python3 --version
            command python3 -m test.run
            echo "----------"

        fi
    fi
}

test $1 $2
