package invoicesm;


/**
 * Klasa reprezentujaca pozycje na fakturze
 * @author Jan Poreba
 *
 */
public class Order {
	/**
	 * produkt/usluga
	 * @see Item
	 */
	private Item item;
	/**
	 * ilosc zakupionego produktu
	 */
	private double amount;
	
	/**
	 * Konstruktor klasy Order
	 * @param itemName nazwa produktu/uslugi
	 * @param itemPrice cena produktu
	 * @param amount ilosc produktu
	 * @throws InvalidOrderException wyjatek rzucany
	 * w przypadku niepoprawnych danych pozycji
	 * @throws InvalidItemException wyjatek rzucany
	 * w przypadku niepoprawnych danych produktu/uslugi
	 */
	public Order(String itemName, double itemPrice, double amount) 
			throws InvalidOrderException, InvalidItemException {
		
		if(amount <= 0) {
			throw new InvalidOrderException("Nieprawidlowa ilosc towaru");
		}
		/*GRASP Creator
		 * Obiekt klasy Item jest tworzony w klasie Order
		 * Klasa Order posiada i bezposrednio uzywa 
		 * obiektow klasy Order
		 */
		
		this.item =  new Item(itemName, itemPrice);
		this.amount = amount;
	}

	/**
	 * @return produkt/usluga
	 */
	public Item getItem() {
		return item;
	}

	/**
	 * @return ilosc
	 */
	public double getAmount() {
		return amount;
	}

	/**
	 * @param produkt
	 * @throws InvalidItemException wyjatek rzucany 
	 * w przypadku niepoprawnych danych produktu
	 */
	public void setItem(String itemName, double itemPrice) throws InvalidItemException {
		this.item = new Item(itemName, itemPrice);
	}

	/**
	 * @param ilosc
	 * @throws InvalidOrderException wyjatek rzucany
	 * w przypadku niepoprawnych danych pozycji
	 */
	public void setAmount(double amount) throws InvalidOrderException {
		if(amount <= 0) {
			throw new InvalidOrderException("Nieprawidlowa ilosc towaru");
		}
		this.amount = amount;
	}
	
	
	/*
	 * GRASP Expert
	 * Klasa Order posiada dane potrzebne do
	 * policzenia ceny czastkowej pozycji
	 * 
	 */
	/**
	 * metoda liczaca cene czastkowa
	 * pozycji na fakturze
	 * @return cena czastkowa pozycji
	 */
	public double patchyPrice() {
		double patchyPrice = amount*item.getPrice();
		return 1.0 * Math.round(100 * patchyPrice) / 100.0;
	}
	
	
	

}
