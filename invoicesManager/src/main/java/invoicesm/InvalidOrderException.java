package invoicesm;



/**
 * Wyjatek rzucany w przypadku niepoprawnych
 * danych pozycji 
 * @see Order
 * @author Jan Poreba
 *
 */
public class InvalidOrderException extends Exception {


	
	private static final long serialVersionUID = 1L;

	/**
	 * Konstruktor podstawowy
	 * @param message komuniakt bledu
	 */
	public InvalidOrderException(String message) {
		super(message);
	}

}
