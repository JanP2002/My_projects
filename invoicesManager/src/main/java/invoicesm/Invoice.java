package invoicesm;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.LinkedList;





/**
 * Klasa reprezentujaca Fakture
 * @author Jan Poreba
 *
 */
public class Invoice {
	/**
	 * Id Faktury
	 */
	private String invoiceId;
	/**
	 * nabywca, firma kupujaca
	 * @see Company
	 */
	private Company purchasingCompany;
	/**
	 * firma sprzedajaca
	 * @see Company
	 */
	private Company sellingCompany;
	/**
	 * napis reprezentujacy
	 * data wystawienia faktury
	 */
	private String date;
	/**
	 * lista pozycji na fakturze
	 */
	private LinkedList<Order> orderList;
	
	
	/**
	 * obiekt reprezentujacy date
	 *  wystawienia faktury
	 */
	private LocalDate dateObj;
	/*
	 * Obiekt formatu daty
	 */
	private DateTimeFormatter dateFormat;
	
	
	/**
	 * Konstuktor klasy Invoice
	 * @param purchasingCompanyId id nabywcy
	 * @param purchasingCompanyName nazwa nabywcy
	 * @param purchasingCompanyAddress adres nabywcy
	 * @param sellingCompanyId id sprzedawcy
	 * @param sellingCompanyName nazwa sprzedawcy
	 * @param sellingCompanyAddress adres sprzedawcy
	 * @param datObj obiekt daty wsytawienia faktury
	 * @throws InvalidCompanyException wyjatek rzucany 
	 * w przypadku niepoprawnych danych firmy
	 */
	public Invoice(String purchasingCompanyId, String purchasingCompanyName, String purchasingCompanyAddress,
			String sellingCompanyId, String sellingCompanyName, String sellingCompanyAddress,
			LocalDate datObj) throws  InvalidCompanyException {
		
		
		
		
		
		this.purchasingCompany = new Company(purchasingCompanyId, purchasingCompanyName, 
				purchasingCompanyAddress);
		this.sellingCompany = new Company(sellingCompanyId, sellingCompanyName, 
				sellingCompanyAddress);
		this.dateObj = datObj;
		this.dateFormat = DateTimeFormatter.ofPattern("dd.MM.yyyy");
		this.date = dateObj.format(dateFormat);
		String y = date.substring(6,10);
		String m = date.substring(3,5);
		this.invoiceId = IdGenerator.getInstance().generateInvoiceId(purchasingCompany.getCompanyId(),y,m);
		this.orderList = new LinkedList<>();
	}
	
	
	/**
	 * Przeciazany konstuktor klasy Invoice
	 * tworzacy fakture z dzisiejsza data
	 * @param purchasingCompanyId id nabywcy
	 * @param purchasingCompanyName nazwa nabywcy
	 * @param purchasingCompanyAddress adres nabywcy
	 * @param sellingCompanyId id sprzedawcy
	 * @param sellingCompanyName nazwa sprzedawcy
	 * @param sellingCompanyAddress adres sprzedawcy
	 * @throws InvalidCompanyException wyjatek rzucany 
	 * w przypadku niepoprawnych danych firmy
	 */
	public Invoice(String purchasingCompanyId, String purchasingCompanyName, String purchasingCompanyAddress,
			String sellingCompanyId, String sellingCompanyName, String sellingCompanyAddress) 
			throws InvalidCompanyException {
		
		this(purchasingCompanyId, purchasingCompanyName, purchasingCompanyAddress,
				sellingCompanyId, sellingCompanyName, sellingCompanyAddress, getCurrentDate());
		
	}
	
	
	
	
	/**
	 * 
	 * @return id faktury
	 */
	public String getInvoiceId() {
		return invoiceId;
	}
	
	/**
	 * 
	 * @return nabywca
	 */
	public Company getPurchasingCompany() {
		return purchasingCompany;
	}
	
	/**
	 * @return sprzedawca
	 */
	public Company getSellingCompany() {
		return sellingCompany;
	}
	

	/**
	 * 
	 * @return napis reprezentujacy date 
	 * wystawienia faktury
	 */
	public String getDate() {
		return date;
	}
	
	
	/**
	 * 
	 * @return lista pozycji na fakturze
	 */
	public LinkedList<Order> getOrderList() {
		return orderList;
	}
	
	
	

	
	/**
	 * 
	 * @param purchasingCompanyId id nabywcy
	 * @param purchasingCompanyName nazwa nabywcy
	 * @param purchasingCompanyAddress adres nabywcy
	 * @throws InvalidCompanyException wyjatek rzucany
	 * w przypadku niepoprawnych danych firmy
	 */
	public void setPurchasingCompany(String purchasingCompanyId, String purchasingCompanyName, 
			String purchasingCompanyAddress) throws InvalidCompanyException {
		this.purchasingCompany = new Company(purchasingCompanyId, purchasingCompanyName, 
				purchasingCompanyAddress);
	}
	
	/**
	 * 
	 * @param purchasingCompanyId id sprzedawcy
	 * @param purchasingCompanyName nazwa sprzedawcy
	 * @param purchasingCompanyAddress adres sprzedawcy
	 * @throws InvalidCompanyException wyjatek rzucany
	 * w przypadku niepoprawnych danych firmy
	 */
	public void setSellingCompany(String sellingCompanyId, String sellingCompanyName, 
			String sellingCompanyAddress) throws InvalidCompanyException {
		this.purchasingCompany = new Company(sellingCompanyId, sellingCompanyName, 
				sellingCompanyAddress);
	}

	


	/**
	 * 
	 * @return metoda statyczna zwracajaca dzisiejsza date
	 */
	private static LocalDate getCurrentDate() {
		LocalDate date = LocalDate.now();
		return date;
		
	}
	

	/**
	 * metoda dodajaca pozycje do faktury
	 * @param order pozycja do dodania do faktury
	 */
	public void addOrder(Order order) {
		orderList.add(order);
	}
	
	
	

	/**
	 * Grasp Expert klasa Invoice posiada dane
	 * do policzenia calkowitej kwoty do zaplaty,
	 * ale w metodzie countFullCost(), nie musimy sie
	 * odwolywac do ceny z klasy Item,
	 * poniewaz w klasie Order mamy metode liczaca
	 * cene czastkowa pozycji, mamy wspolprace
	 * expertow oraz nieskie sprzezenie (GRASP)
	 */
	/**
	 * Metoda liczaca calkowita kwote do zaplaty faktury
	 * @return calkowita kwota do zaplaty
	 * @see Order#patchyPrice()
	 */
	public double countFullCost() {
		double fullCost = 0;
		for(Order order : orderList ) {
			fullCost += order.patchyPrice();
		}
		return 1.0 * Math.round(100 * fullCost) / 100.0;
	}
	
	
	

}
