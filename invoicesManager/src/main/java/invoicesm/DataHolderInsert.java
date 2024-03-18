package invoicesm;

/**
 * Klasa odpowiedzialna za wstawianie
 * danych do DataHoldera
 * wybranym przez nas obiektem jest DataHolder imitujacy
 * baze danych
 * GRASP PureFabrication klasa odpoweidzlana za
 * wstawianie danych
 */
public class DataHolderInsert implements DAOInsertIF{

	/**
	 * metoda wstawiajaca firme do DataHoldera
	 * @param company firma, ktora chcemy wstawic
	 */
	@Override
	public void insertCompany(Company company) {
		DataHolder.getInstance().insertCompany(company);
	}
	/**
	 * metoda wstawiajaca fakture do DataHoldera
	 * @param invoice faktura, ktora chcemy wstawic
	 */
	@Override
	public void insertInvoice(Invoice invoice) {
		DataHolder.getInstance().insertInvoice(invoice);
		
	}
	/**
	 * metoda wstawiajaca produkt do DataHoldera
	 * @param item produkt, ktory chcemy wstawic
	 */
	@Override
	public void insertItem(Item item) {
		DataHolder.getInstance().insertItem(item);
		
	}

}
