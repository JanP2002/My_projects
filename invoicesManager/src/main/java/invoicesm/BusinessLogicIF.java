package invoicesm;

import java.util.List;


/**
* Interfejs logiki biznesowej,
* metody interfejsu na podstawie polecen z aplikacji
* wywoluja metody wykonujace
* operacje na bazie danych
* GRASP Polimofrizm
*/
public interface BusinessLogicIF {
	
	/**
	 * metoda wstawiajaca firme do bazy danych
	 * @param company referencja do firmy
	 */
	public void insertCompany(Company comapny);
	/**
	 * metoda wstawiwajaca produkt do bazy danych
	 * @param referencja do produktu
	 */
	public void insertItem(Item item);
	/**
	 * metoda wstawiwajaca fakture do bazy danych
	 * @param referencja do faktury
	 */
	public void insertInvoice(Invoice invoice);
	/**
	 * metoda wstawiajaca wszytkie produkty z faktury
	 * do bazy danych
	 * @param orderList lista pozycji na fakturze
	 */
	public void insertInvoiceItems(List<Order> orderList);
	/**
	 * metoda odczytujaca liste faktur z bazy danych
	 * @return lista faktur zapisanych w bazie danych
	 */
	public List<Invoice> readInvoiceList();
	
	
	
	

}
