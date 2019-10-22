class Employee:
    '所有员工的基类'
    empCount = 0

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        Employee.empCount += 1

    def displayCount(self):
        print("Total Employee %d" % Employee.empCount)

    def displayEmployee(self):
        print("name : ", self.name, ",  salary : ", self.salary)


if __name__ == "__main__":
    t = Employee('aaa', 1)
    t.displayEmployee()
    b = Employee("bbb", 3244)
    b.displayEmployee()
    print("empCount : %d " % Employee.empCount)

    print(hasattr(Employee, "address"))
    setattr(Employee, "address", "北京大栅栏")
    print(getattr(Employee, "address"))
    delattr(Employee, "address")

    print("Employee.__doc__:", Employee.__doc__)
    print("Employee.__name__:", Employee.__name__)
    print("Employee.__module__:", Employee.__module__)
    print("Employee.__bases__:", Employee.__bases__)
    print("Employee.__dict__:", Employee.__dict__)
