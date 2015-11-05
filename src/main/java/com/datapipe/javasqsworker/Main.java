package com.datapipe.javasqsworker;

public class Main {

    private static void sleep() {
        try {
            Thread.sleep(5000);
        } catch(InterruptedException ex) {
            Thread.currentThread().interrupt();
        }
    }

    public static void main(String[] args) throws Exception {
        System.out.println("Test app starting up.");

        // "work"
        for (int i = 0; i < 10; i++) {
            System.out.println(String.format("%s of 10: working...", i));
            sleep();
        }

        //throw new Exception("whoops something went wrong!");

        System.out.println("Done processing.");
    }
}
