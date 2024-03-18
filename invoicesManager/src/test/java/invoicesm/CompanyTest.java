package invoicesm;

import static org.junit.Assert.*;

import org.junit.Test;

/**
 * Test jednostkowy klasy Company
 * @author Jan Poreba
 *
 */
public class CompanyTest {

	/**
	 * Testowanie tworzenia obiektu klasy Company,
	 * gdy dane firmy sa poprawne
	 * @throws InvalidCompanyException wyjatek rzucany
	 * w przypadku niepoprawnych danych
	 * firmy
	 */
	@Test
	public void testNonException() throws InvalidCompanyException {
		new Company("1111111111", "sampleCompany", "Wrocław ul. Sienkiewicza 1");
	}
	
	/**
	 * Testowanie tworzenia obiektu klasy Company,
	 * gdy dane firmy nie sa poprawne
	 * @throws InvalidCompanyException wyjatek rzucany
	 * w przypadku niepoprawnych danych
	 * firmy
	 */
	@Test(expected = InvalidCompanyException.class)
	public void testExpectedException() throws InvalidCompanyException {
		new Company("1111111111", "sampleCompany","");
	}

}
