package invoicesm;

import static org.junit.Assert.*;

import org.junit.Test;


/**
 * Test jednostkowy tworzenia faktury
 */
public class InvoiceCreationTest {

	/**
	 * Testowanie tworzenia faktury, gdy
	 * dane faktury sa poprawne
	 * @throws InvalidCompanyException wyjatek rzucany
	 * w przypadku niepoprawnych danych firmy
	 */
	@Test
	public void testNonException() throws InvalidCompanyException {
		String puchasingCompanyName = "myCompany";
		String purchasingCompanyId = "1111111111";
		String purchasingCompanyAddress =
				"Wrocław ul. Norwida 1";
		String sellingCompanyName = "yourCompany";
		String sellingCompanyId = "2111111111";
		String sellingCompanyAddress =
				"Wrocław ul. Sienkiewicza 3";
		
		new Invoice(purchasingCompanyId, puchasingCompanyName, purchasingCompanyAddress,
				sellingCompanyId, sellingCompanyName, sellingCompanyAddress);
	}
	
	/**
	 * Testowanie tworzenia faktury, gdy
	 * dane firmy na fakturze
	 * sa niepoprawne
	 * @throws InvalidCompanyException wyjatek rzucany
	 * w przypadku niepoprawnych danych firmy
	 */
	@Test(expected = InvalidCompanyException.class)
	public void testExpectedException() throws InvalidCompanyException {
		String puchasingCompanyName = "myCompany";
		String purchasingCompanyId = "";
		String purchasingCompanyAddress =
				"Wrocław ul. Norwida 1";
		String sellingCompanyName = "yourCompany";
		String sellingCompanyId = "2111111111";
		String sellingCompanyAddress =
				"Wrocław ul. Sienkiewicza 3";
		
		new Invoice(purchasingCompanyId, puchasingCompanyName, purchasingCompanyAddress,
				sellingCompanyId, sellingCompanyName, sellingCompanyAddress);
	}

}
