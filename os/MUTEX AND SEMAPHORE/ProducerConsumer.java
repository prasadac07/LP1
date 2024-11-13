
import java.util.Queue;
import java.util.LinkedList;

import java.util.concurrent.Semaphore;

public class ProducerConsumer {

	private static Queue<Integer> buffer = new LinkedList<Integer>();
	private static Semaphore empty = new Semaphore(4);
	private static Semaphore full = new Semaphore(0);
	private static Semaphore mutex = new Semaphore(1);
	private static int value = 0;
	
	static class Producer implements Runnable{
		@Override
		public void run() {
			try {
				while (true) {
					empty.acquire();
					mutex.acquire();
					Thread.sleep(1000);
					int item = produceItem();
					buffer.add(item);
					mutex.release();
					full.release();
				}
			} catch (InterruptedException e) {
				System.out.println(e.getMessage());
			}
		}
		
		private int produceItem() {
			value++;
			System.out.println("Produced item: " + value);
			return value;
		}
	}
	
	static class Consumer implements Runnable {
		@Override
		public void run() {
			try {
				while (true) {
					full.acquire();
					mutex.acquire();
					buffer.poll();
					mutex.release();
					empty.release();
					Thread.sleep(7000);
					consumeItem();
				}
			} catch (InterruptedException e) {
				System.out.println(e.getMessage());
			}
		}
		
		private void consumeItem() {
			System.out.println("Item Consumed: " + value);
			value--;
		}
	}
	
	public static void main(String[] args) {
		Thread producer1 = new Thread(new Producer());
		Thread consumer = new Thread(new Consumer());
		
		producer1.start();
		consumer.start();
	}
}
