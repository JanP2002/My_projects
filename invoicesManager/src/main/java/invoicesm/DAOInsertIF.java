package invoicesm;


/**
 * Interfejs odpowiedzialny za wstawianie danych
 * do bazy
 * Dependacy Inversion zaleznosc od interfejsu, 
 * a nie rodzaju bazy danych
 * mozemy dzieki temu w latwy sposb zmienic rodzaj 
 * bazy danych
 */
public interface DAOInsertIF {
	/**
	 * metoda wstawiwjaca firme do bazy danych
	 * @param company firma ktora wstawiamy do bazy
	 */
	public void insertCompany(Company company);
	/**
	 * meroda wstawiajaca fakture do bazy danych
	 * @param invoice faktura ktora wstawiamy do bazy
	 */
	public void insertInvoice(Invoice invoice);
	/**
	 * metoda wstawiajaca produkt do bazy danych
	 * @param item produkt ktory wstawiamy do bazy
	 */
	public void insertItem(Item item);

}
