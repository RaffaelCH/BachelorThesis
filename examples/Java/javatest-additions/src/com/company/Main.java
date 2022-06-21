package com.company;

import com.company.OuterClass.InnerClass;

public class Main {

    public static void main(String[] args) {
	    System.out.println("Hello, world!");

        AbstractImplementation abstr = new AbstractImplementation();
        abstr.abstractFun();

        MyInterface myInt = new InterfaceImplementation();
        myInt.test();

        OuterClass outer = new OuterClass();
        InnerClass inner = outer.new InnerClass();
        outer.outer();
        inner.inner();

        SuperClass sup = new SuperClass();
        sup.superMethod();
        SubClass sub = new SubClass();
        sub.subMethod();
    }
}
