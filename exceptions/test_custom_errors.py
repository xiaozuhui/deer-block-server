from exceptions.code_error import CodeError

if __name__ == "__main__":
    err = CodeError('ErrCodeType')
    print(err)
    # err = CodeError("ErrCodeType")
    # print(err)
    # print(CodeError("ErrCodeType").to_serializer())
    ser = CodeError.ErrCodeType.to_serializer()
    print(ser)
    # raise err
