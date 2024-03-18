package invoicesm;

import java.util.LinkedList;


/**
 * klasa DataHolder wzorca Singleton sluzaca do 
 * przechowywania danych o fakturach, firmach i produktach/uslugach
 * imituje ona baze danych
 */
public class DataHolder {
	
	
	/**
	 * lista firm
	 */
	private LinkedList<Company> companyList;
	/**
	 * lista faktur
	 */
	private LinkedList<Invoice> invoiceList;
	/**
	 * lista produktow
	 */
	private LinkedList<Item> itemList;
	
	
	/**
     * prywatny konstruktor klasy DataHolder
     * klasa DataHolder ma tylko jeden egzemplarz globalnie dostepny
     */
	private DataHolder() {
		companyList = new LinkedList<Company>();
		invoiceList = new LinkedList<Invoice>();
		itemList = new LinkedList<Item>();
		
	}
	
	/**
     * Tworzenie obiektu klasy DataHolder
     */
    private static DataHolder instance = new DataHolder();
    
    /**
     * Zwracanie jedynego dostepnego obiektu klasy DataHolder
     * @return jedyny dostepny obiekt klasy DataHolder
     */
    public static DataHolder getInstance(){
        return instance;
    }
    
    
   


	/**
	 * @return lista firm
	 */
	public LinkedList<Company> getCompanyList() {
		return companyList;
	}



	/**
	 * @return lista faktur
	 */
	public LinkedList<Invoice> getInvoiceList() {
		return invoiceList;
	}



	/**
	 * @return lista produktow
	 */
	public LinkedList<Item> getItemList() {
		return itemList;
	}

    
    
    
	/**
	 * metoda wstawiajaca firme do listy firm
	 * @param company firma, ktora chcemy wstawic
	 */
    public void insertCompany(Company company) {
    	companyList.add(company);
    }
    
    /**
     * metoda wstawiajaca fakture do listy faktur
     * @param invoice faktura, ktora chcemy wstawic
     */
    public void insertInvoice(Invoice invoice)  {
    	invoiceList.add(invoice);
    }
    
    /**
     * metoda wstawiajaca produkt/usluge do listy produktow
     * @param item produkt, ktory chcemy wstawic
     */
    public void insertItem(Item item)  {
    	itemList.add(item);
    }
    

}
