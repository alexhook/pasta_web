class Test1:
    a = 1

    def main():
        print()
    
    def test():
        print('test')


class Test2:
    def main(self):
        print(self.a)


class NewTest(Test2, Test1):
    pass

NewTest().main()
NewTest.test()