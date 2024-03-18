package invoicesm;

import static org.junit.Assert.*;

import org.junit.Test;



/**
 * Test jednostkowy klasy Item
 * @author Jan Poreba
 *
 */
public class ItemTest {

	/**
	 * Testowanie tworzenia obiektu klasy Item,
	 * gdy dane produktu/uslugi sa poprawne
	 * @throws InvalidItemException wyjatek rzucany
	 * w przypadku niepoprawnych danych
	 * produktu/uslugi
	 */
	@Test
	public void testNonException() throws InvalidItemException {
		new Item("papier", 5.5);
	}
	
	
	/**
	 * Testowanie tworzenia obiektu klasy Item,
	 * gdy dane produktu/usugi nie sa poprawne
	 * @throws InvalidItemException wyjatek rzucany
	 * w przypadku niepoprawnych danych
	 * produktu/uslugi
	 */
	@Test(expected = InvalidItemException.class)
	public void testExpectedException() throws InvalidItemException {
		new Item("papier", -3.4);
	}

}
