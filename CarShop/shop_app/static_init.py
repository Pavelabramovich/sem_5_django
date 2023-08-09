def static_init(cls):
    if getattr(cls, "static_init", None):
        cls.static_init()
    return cls


# def test_static_init():
#     assert SomeEnum.text_dict["Val A"] == SomeEnum.VAL_A
#     assert SomeEnum.text_dict["Val B"] == SomeEnum.VAL_B
#     assert SomeEnum.text_dict["Val C"] == SomeEnum.VAL_C
#     assert SomeEnum.text_dict["Val D"] == SomeEnum.VAL_D