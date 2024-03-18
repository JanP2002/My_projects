package invoicesm;



/**
 * Klasa reprezentujaca produkt/usluge
 * @author Jan Poreba
 *
 */
public class Item {
	/**
	 * id produktu
	 */
	private String itemId;
	/**
	 * nazwa produktu
	 */
	private String name;
	/**
	 * cena produktu
	 */
	private double price;
	
	/**
	 * Konstruktor klasy Item
	 * @param name nazwa produktu
	 * @param price cena produktu
	 * @throws InvalidItemException wyjatek
	 * wywyoywany w przypadku niepoprawnych danych produktu
	 */
	public Item(String name, double price) throws InvalidItemException {
		if(name.equals("")) {
			throw new InvalidItemException("Nie podano nazwy towaru/uslugi");
		}
		
		if(price < 0) {
			throw new InvalidItemException("Nieprawidlowa cena towaru/uslugi");
		}
		
		this.itemId = IdGenerator.getInstance().generateItemId();
		this.name = name;
		this.price = price;
	}


	/**
	 * @return id produktu
	 */
	public String getItemId() {
		return itemId;
	}


	/**
	 * @return nazwa produktu
	 */
	public String getName() {
		return name;
	}


	/**
	 * @return cena produktu
	 */
	public double getPrice() {
		return price;
	}



	/**
	 * @param nazwa produktu
	 * @throws InvalidItemException wyjatek
	 * wywyolywany w przypadku niepoprawnej nazwy produktu
	 */
	public void setName(String name) throws InvalidItemException {
		if(name.equals("")) {
			throw new InvalidItemException("Nie podano nazwy towaru/uslugi");
		}
		this.name = name;
	}


	/**
	 * @param cena produktu
	 * @throws InvalidItemException wyjatek
	 * wywolywany w przypadku niepoprawnej ceny produktu
	 */
	public void setPrice(double price) throws InvalidItemException {
		if(price < 0) {
			throw new InvalidItemException("Nieprawidlowa cena towaru/uslugi");
		}
		this.price = price;
	}
}
