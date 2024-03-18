package invoicesm;



/**
 * Wyjatek rzucany w przypadku niepoprawnych 
 * danych firmy
 * @see Company
 * @author Jan Poreba
 *
 */
public class InvalidCompanyException extends Exception {

	private static final long serialVersionUID = 1L;
	
	/**
	 * Konstruktor podstawowy
	 * @param message komunikat bledu
	 */
	public InvalidCompanyException(String message) {
		super(message);
	}

}
