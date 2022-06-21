package com.company;

public class OuterClass {

    public class InnerClass {
        public void inner() {
            System.out.println("inner");
        }

        public class InnerestClass {
            public void innerest() {
                System.out.println("innerest");
            }
        }
    }

    public void outer() {
        System.out.println("outer");
    }
}
