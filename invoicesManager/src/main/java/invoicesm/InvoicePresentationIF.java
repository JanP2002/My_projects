package invoicesm;

import java.util.List;


/* GRASP Polymorphism
* GRASP Protected Variations
* Mozna stworzyc wiele roznych widokow
* faktury impelementujacych interfejs i 
* w latwy sposob zmnienic
* sposob wyswietlania faktury
*/
/**
* Interfejs prezentacji faktury
* @author Jan Poreba
*
*/
public interface InvoicePresentationIF {
	/**
	 * Metoda generujaca widok faktury
	 * @param invoice faktura
	 * @return napis reprezentujacy widok faktury
	 */
	public String generateInvoiceView(Invoice invoice);
	/**
	 * metoda generujaca widok listy faktur
	 * @param invoiceList lista faktur
	 * @return lista napisow z podstawowymi 
	 * danymi z faktur
	 */
	public List<String> generateInvoiceLabelList(List<Invoice> invoiceList);
}
