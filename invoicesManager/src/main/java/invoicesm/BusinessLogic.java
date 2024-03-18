package invoicesm;

import java.util.List;




/*
 * Dependancy Inversion
 * Warstwa logiki biznesowej zalezy od interjesu
 * bazodanowego, a nie od wybranej bazy danych
 */
/**
 * Klasa logiki biznesowej,
 * na podstawie polecen z aplikacji
 * wywoluje metody wykonujace
 * operacje na bazie danych
 * @author Jan Poreba
 *
 */
public class BusinessLogic implements BusinessLogicIF{

	/**
	 * obiekt odpowiedzialny
	 * za wstawianie danych do bazy
	 */
	private DAOInsertIF daoInsert;
	/**
	 * obiekt odpowiedzialny za
	 * odczytywanie danych z bazy
	 */
	private DAOReadIF daoRead;
	
	/*W latwy sposob mozemy zmienic
	rodzaj bazy danych*/
	public BusinessLogic() {
		daoInsert = new DataHolderInsert();
		daoRead = new DataHolderRead();
	}
	
	/**
	 * metoda wstawiajaca firme do bazy danych
	 * @param company referencja do firmy
	 */
	@Override
	public void insertCompany(Company company) {
		daoInsert.insertCompany(company);
		
	}

	/**
	 * metoda wstawiwajaca produkt do bazy danych
	 * @param referencja do produktu
	 */
	@Override
	public void insertItem(Item item) {
		daoInsert.insertItem(item);
		
	}
	/**
	 * metoda wstawiwajaca fakture do bazy danych
	 * @param referencja do faktury
	 */
	@Override
	public void insertInvoice(Invoice invoice) {
		daoInsert.insertInvoice(invoice);
		
	}
	/**
	 * metoda wstawiajaca wszytkie produkty z faktury
	 * do bazy danych
	 * @param orderList lista pozycji na fakturze
	 */
	@Override
	public void insertInvoiceItems(List<Order> orderList) {
		for(Order order : orderList) {
			Item item = order.getItem();
			insertItem(item);
		}
	}
	/**
	 * metoda odczytujaca liste faktur z bazy danych
	 * @return lista faktur zapisanych w bazie danych
	 */
	@Override
	public List<Invoice> readInvoiceList() {
		return daoRead.readInvoiceList();
		
	}
	

}
