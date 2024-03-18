package invoicesm;

import java.util.List;
/**
 * Interfejs odpowiedzialny za odczytywanie danych z bazy
 * Dependacy Inversion zaleznosc od interfejsu, 
 * a nie rodzaju bazy danych
 * mozemy dzieki temu w latwy sposb zmienic rodzaj 
 * bazy danych
 */
public interface DAOReadIF {
	/**
	 * metoda odczytujaca liste faktur zapisanych w bazie
	 * @return lista faktur zapisanych w bazie
	 */
	public List<Invoice> readInvoiceList();
	

}
