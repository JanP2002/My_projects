package invoicesm;


/**
 * pomocnicza klasa przechowujaca 
 * dane pojedynczej pozycji na fakturze
 */
public class OrderView {

	private String itemName;
	private double itemPrice;
	private double amount;
	private double patchyPrice;
	
	/**
	 * Konstuktor klasy OrderView
	 * @param order pozycja na fakturze
	 */
	public OrderView(Order order) {
		Item item = order.getItem();
		this.itemName = item.getName();
		this.itemPrice = item.getPrice();
		this.amount = order.getAmount();
		this.patchyPrice= order.patchyPrice();
	}


	/**
	 * @return nazwa produktu
	 */
	public String getItemName() {
		return itemName;
	}


	/**
	 * @return the cena produktu
	 */
	public double getItemPrice() {
		return itemPrice;
	}


	/**
	 * @return ilosc zakupionego produktu
	 */
	public double getAmount() {
		return amount;
	}


	/**
	 * @return cena czastkowa za zakup produktu
	 */
	public double getPatchyPrice() {
		return patchyPrice;
	}


	/**
	 * @param itemName nazwa produktu
	 */
	public void setItemName(String itemName) {
		this.itemName = itemName;
	}


	/**
	 * @param itemPrice cena produktu
	 */
	public void setItemPrice(double itemPrice) {
		this.itemPrice = itemPrice;
	}


	/**
	 * @param amount ilosc produktu
	 */
	public void setAmount(double amount) {
		this.amount = amount;
	}


	/**
	 * @param patchyPrice cena czastkowa 
	 * pozycji na fakturze
	 */
	public void setPatchyPrice(double patchyPrice) {
		this.patchyPrice = patchyPrice;
	}
}
