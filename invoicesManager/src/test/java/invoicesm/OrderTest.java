package invoicesm;

import static org.junit.Assert.*;

import org.junit.Test;



/**
 * Test jednostkowy klasy Order
 * @author Jan Poreba
 *
 */
public class OrderTest {

	/**
	 * Testowanie tworzenia obiektu klasy Order,
	 * gdy dane pozycji na fakturze sa poprawne
	 * @throws InvalidOrderException wyjatek rzucany
	 * w przypadku niepoprawnych danych
	 * pozycji
	 * * @throws InvalidItemException wyjatek rzucany
	 * w przypadku niepoprawnych danych
	 * produktu/uslugi
	 */
	@Test
	public void testNonException() throws InvalidOrderException, InvalidItemException {
		Order order = new Order("papier",5.5, 2);
		double expectedResult = 11;
		assertEquals(expectedResult, order.patchyPrice(),0);
	}
	
	
	/**
	 * Testowanie tworzenia obiektu klasy Order,
	 * gdy dane produktu pozycji sa niepoprawne
	 * @throws InvalidOrderException wyjatek rzucany
	 * w przypadku niepoprawnych danych
	 * pozycji
	 * * @throws InvalidItemException wyjatek rzucany
	 * w przypadku niepoprawnych danych
	 * produktu/uslugi
	 */
	@Test(expected = InvalidItemException.class)
	public void testExpectedItemException() throws InvalidItemException, InvalidOrderException {
		new Order("papier",-3.5, 2);
	}
	
	
	 /**
	 * Testowanie tworzenia obiektu klasy Order,
	 * gdy dane pozycji sa niepoprawne
	 * @throws InvalidOrderException wyjatek rzucany
	 * w przypadku niepoprawnych danych
	 * pozycji
	 * * @throws InvalidItemException wyjatek rzucany
	 * w przypadku niepoprawnych danych
	 * produktu/uslugi
	 */
	@Test(expected = InvalidOrderException.class)
	public void testExpectedOrderException() throws InvalidItemException, InvalidOrderException {
		new Order("papier",3.5, 0);
	}

}
