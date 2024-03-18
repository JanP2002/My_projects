package invoicesm;

import static org.junit.Assert.*;

import org.junit.Test;

/**
 * Test jednostkowy liczenia
 * calkowitej kwoty do zaplaty za 
 * fakture
 */
public class TestCountingFullCost {

	/**
	 * Testowanie liczenia calkowitej kwoty
	 * do zaplaty
	 * @throws InvalidCompanyException wyjatek
	 * rzucany w przypadku niepoprawnych danych firmy
	 * @throws InvalidOrderException wyjatek rzucany
	 * w przypadku niepoprawnych danych
	 * pozycji na fakturze
	 * @throws InvalidItemException wyjatek rzucany w
	 * przypadku niepoprawnych danych produktu
	 */
	@Test
	public void testCountingFullCost() 
			throws InvalidCompanyException, InvalidOrderException, InvalidItemException {
		String puchasingCompanyName = "myCompany";
		String purchasingCompanyId = "1111111111";
		String purchasingCompanyAddress =
				"Wrocław ul. Norwida 1";
		String sellingCompanyName = "yourCompany";
		String sellingCompanyId = "2111111111";
		String sellingCompanyAddress =
				"Wrocław ul. Sienkiewicza 3";
		
		Invoice invoice = new Invoice(purchasingCompanyId, puchasingCompanyName, purchasingCompanyAddress,
				sellingCompanyId, sellingCompanyName, sellingCompanyAddress);
		
		Order paperOrder = new Order("papier", 12.5,4);
		Order penOrder = new Order("dlugopis",2.5,4);
		
		invoice.addOrder(penOrder);
		invoice.addOrder(paperOrder);
		
		double expectedResult = 60;
		double fullCost = invoice.countFullCost();
		
		assertEquals(expectedResult, fullCost,0);
		
		
	}
	
	/**
	 * Testowanie liczenia calkowitej kwoty
	 * do zaplaty w przypadku braku pozycji
	 * na fakturze
	 * @throws InvalidCompanyException wyjatek
	 * rzucany w przypadku niepoprawnych danych firmy
	 * @throws InvalidOrderException wyjatek rzucany
	 * w przypadku niepoprawnych danych
	 * pozycji na fakturze
	 * @throws InvalidItemException wyjatek rzucany w
	 * przypadku niepoprawnych danych produktu
	 */
	@Test
	public void testZeroCost() 
			throws InvalidCompanyException, InvalidOrderException, InvalidItemException {
		String puchasingCompanyName = "myCompany";
		String purchasingCompanyId = "1111111111";
		String purchasingCompanyAddress =
				"Wrocław ul. Norwida 1";
		String sellingCompanyName = "yourCompany";
		String sellingCompanyId = "2111111111";
		String sellingCompanyAddress =
				"Wrocław ul. Sienkiewicza 3";
		
		Invoice invoice = new Invoice(purchasingCompanyId, puchasingCompanyName, purchasingCompanyAddress,
				sellingCompanyId, sellingCompanyName, sellingCompanyAddress);
		
		
		double expectedResult = 0;
		double fullCost = invoice.countFullCost();
		
		assertEquals(expectedResult, fullCost,0);
		
		
	}

}
