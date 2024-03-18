package invoicesm;

import java.util.List;

/**
 * Klasa odpowiedzialna za odczytywanie 
 * danych z DataHoldera
 * wybranym przez nas obiektem jest DataHolder imitujacy
 * baze danych
 * GRASP PureFabrication klasa odpoweidzlana za
 * odczytywanie danych
 */
public class DataHolderRead implements DAOReadIF{

	/**
	 * metoda odczytujaca wszystkie faktury z bazy danych 
	 * @return lista faktur zapisanych w bazie danych
	 */
	@Override
	public List<Invoice> readInvoiceList() {
		return DataHolder.getInstance().getInvoiceList();
	}
	
	

}
