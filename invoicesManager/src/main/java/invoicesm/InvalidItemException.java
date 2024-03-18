package invoicesm;



public class InvalidItemException extends Exception {

	/**
	 * Wyjatek rzucany w przypadku niepoprawnych 
	 * danych produktu/uslugi
	 * @author Jan Poreba
	 * @see Item
	 *
	 */
	private static final long serialVersionUID = 1L;
	
	/**
	 * Konstruktor podstawowy
	 * @param message komunikat bledu
	 */
	public InvalidItemException(String message) {
		super(message);
	}

}
