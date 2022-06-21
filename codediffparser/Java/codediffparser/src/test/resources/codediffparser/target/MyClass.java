package codediffparser.testclasses;

import java.util.ArrayList;
import java.util.List;

import codediffparser.inner.MyOtherClass;

public class MyClass {
    private Ibaz m_something = new MyInnerClass();

    public interface Ibaz {
        void trick();
    }

    public void foo(Class<? extends Ibaz> clazz) {
        MyOtherClass.foo();
        List<String> blubb = new ArrayList<>();
        blubb.add(bar("test"));
    }

    protected String bar(String s) {
        foo(m_something.getClass());
        return s;
    }
}
