import java.util.concurrent.Semaphore;


public class ReaderWriter {
	
	static Semaphore mutex = new Semaphore(1);
	static Semaphore wrt = new Semaphore(1);
	static int readcount = 0;
	
	static String message = "message";
	
	static class Writer implements Runnable {
		@Override
		public void run() {
			try {
				wrt.acquire();
				message = Thread.currentThread().getName() + " message";
				System.out.println(Thread.currentThread().getName() + " writing...");
				Thread.sleep(1500);
				System.out.println(Thread.currentThread().getName() + " written.");
				wrt.release();	
			}
			catch(InterruptedException e) {
				System.out.println(e.getMessage());
			}
		}
	}
	
	static class Reader implements Runnable {
		@Override
		public void run() {
			try {
				mutex.acquire();
				readcount++;
				if(readcount == 1) {
					wrt.acquire();
				}
				mutex.release();
				System.out.println(Thread.currentThread().getName() + " reading...");
				System.out.println(message);
				Thread.sleep(1000);
				System.out.println(Thread.currentThread().getName() + " read.");
				mutex.acquire();
				readcount--;
				if(readcount == 0) {
					wrt.release();
				}
				mutex.release();
			} catch (InterruptedException e) {
				e.getMessage();
			}
		}
	}

	public static void main(String[] args) {
		Reader reader = new Reader();
		Writer writer = new Writer();
		
		Thread r1 = new Thread(reader);
		r1.setName("Reader 1");
		Thread r2 = new Thread(reader);
		r2.setName("Reader 2");
		Thread r3 = new Thread(reader);
		r3.setName("Reader 3");
		
		
		Thread w1 = new Thread(writer);
		w1.setName("Writer 1");
		Thread w2 = new Thread(writer);
		w2.setName("Writer 2");
		Thread w3 = new Thread(writer);
		w3.setName("Writer 3");
		
		w1.start();
		r1.start();
		r2.start();
		w2.start();
		r3.start();
		w3.start();
	}

}
