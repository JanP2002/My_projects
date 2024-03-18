package invoicesm;

import java.util.LinkedList;
import java.util.List;




/* GRASP wysoka spojnosc 
* Widok faktury nie jest tworzony w klasie GUI,
* tylko w oddzielnej klasie
*/
/**
* Klasa odpowiedzialna za widok 
* wyswitlanej faktury
* @see InvoicePresentationIF
* @author Jan Poreba
*
*/
public class InvoicePresentation implements InvoicePresentationIF{

	/**
	 * Metoda formatujaca napis do odpowiedniej dlugosci
	 * @param string napis
	 * @param length dlugosc do jakiej 
	 * chcemy sformatowac napis
	 * @return napis sformatowany do wybranej dlugosci
	 */
	private String formatString(String string, int length) {
		String formattedString = string;
		int stringSize = string.length();
		if(stringSize < length) {
			for(int i = stringSize ; i < length; i++) {
				formattedString += " ";
			}
		}
		else if(stringSize > length) {
				formattedString = string.substring(0,length);
			}
		return formattedString;
		
	}
	
	 /**
	 * Metoda generujaca kreske,
	 * napis z myslnikami
	 * @param n ilosc myslnikow, ktore chcemy
	 * ustawic
	 * @return napis z n myslnikami, kreska 
	 * o dlugosci n
	 */
	private String dashesString(int n) {
		String dashesString ="";
		for(int i = 0; i < n; i++) {
			dashesString +="-";
		}
		return dashesString;
	}
	
	
	/**
	 * Metoda generujaca widok wyswietlanej faktury
	 * @param invoice faktura
	 * @return napis reprezentujacy widok faktury
	 * 
	 */
	@Override
	public String generateInvoiceView(Invoice invoice) {
		String invoiceView = "";
		invoiceView +="Faktura nr: " + invoice.getInvoiceId() + formatString("",40) +
				invoice.getDate()+"\n" +"\n";
		invoiceView += formatString("Sprzedawca:",50) + "Nabywca:" + "\n";
		Company sellingCompany = invoice.getSellingCompany();
		Company purchasingCompany =invoice.getPurchasingCompany();
		invoiceView += formatString(sellingCompany.getCompanyName(),50) + 
				purchasingCompany.getCompanyName() + "\n";
		invoiceView += formatString(sellingCompany.getAddress(),50) + 
				purchasingCompany.getAddress() + "\n";
		invoiceView += formatString(sellingCompany.getCompanyId(),50) + 
				purchasingCompany.getCompanyId() + "\n";
		
		
		invoiceView += "\n" + "\n";
		invoiceView += dashesString(100) + "\n";
		invoiceView += formatString("Lp",3) + "| " +  formatString("Nazwa produktu",30) + 
				"| " + formatString("Cena",8)+ "| " + formatString("ilośc",8) + "| " + 
				formatString("Koszt",8) + "\n";
		invoiceView += dashesString(100) + "\n";
		LinkedList<Order> orderList = invoice.getOrderList();
		int i = 1;
		for(Order order : orderList) {
			Item item = order.getItem();
			invoiceView += formatString(Integer.toString(i),3) + "| "  +  formatString(item.getName(),30) + 
					"| " + formatString(Double.toString(item.getPrice()) + " zł",8)+ "| " + 
					formatString(Double.toString(order.getAmount()),8) + "| " + 
					formatString(Double.toString(order.patchyPrice()) + " zł",8) + "\n";
			invoiceView += dashesString(100) + "\n";
			i++;
		}
		invoiceView += "Kwota do zapłaty: " + Double.toString(invoice.countFullCost()) + " zł" ;
		
				
		return invoiceView;
	}

	/**
	 * metoda generujaca widok listy faktur
	 * @param invoiceList lista faktur
	 * @return lista napisow z podstawowymi 
	 * danymi z faktur
	 */
	@Override
	public List<String> generateInvoiceLabelList(List<Invoice> invoiceList) {
		List<String> invoiceLabels = new LinkedList<String>();
		for(Invoice invoice : invoiceList) {
			String currentLabel = 
				formatString(invoice.getInvoiceId(), 10) + "  |  " + formatString(invoice.getPurchasingCompany().getCompanyName(), 10) + "  |  " +
				formatString(invoice.getSellingCompany().getCompanyName(), 10) + "  |  " + invoice.getDate();
			invoiceLabels.add(currentLabel);
		}
		return invoiceLabels;
	}

	

}
