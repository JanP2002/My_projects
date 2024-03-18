package invoicesm;



/**
 * Grasp wysoka spojnosc
 * Id jest generowane przez IdGenerator,
 * a nie bezposrednio przez klasy Item, czy Invoice
 */
/**
 * Klasa wzorca singleton generujaca id
 * @author Jan Poreba
 *
 */
public class IdGenerator {

	/**
	 * licznik faktur
	 */
	private static int invoiceIdCounter;
	/**
	 * licznik produktow/uslug
	 */
	private static int itemIdCounter;
	/**
	 * Tworzenie obiektu klasy IdGenerator
	 */
	private static IdGenerator instance = new IdGenerator();
	
	/**
     * Prywatny konstruktor klasy IdGenerator
     * klasa IdGenerator ma tylko jeden egzemplarz globalnie dostepny
     */
	private IdGenerator() {
		invoiceIdCounter = 0;
		itemIdCounter = 0;
	}
	
	
	/**
     * Zwracanie jedynego dostepnego obiektu klasy IdGenerator
     * @return jedyny dostepny obiekt klasy IdGenerator
     */
	public static IdGenerator getInstance(){
        return instance;
    }
	
	
	/**
	 * Metoda generujaca id faktury
	 * @param companyId id firmy nabywajacej
	 * @param year rok wystawienia faktury
	 * @param month miesiac wystawienia faktury
	 * @return id faktury
	 */
	 public String generateInvoiceId(String companyId, String year, String month){
	    invoiceIdCounter++;
	    String invoiceCounter = Integer.toString(invoiceIdCounter-1);
	    String formattedCounter = String.format("%6s", invoiceCounter).replace(' ', '0');
	    return companyId + "/" + formattedCounter + "/" +
	    year + "/" + month;
	 }
	 
	 /**
	  * Metoda generujaca id produktu/uslugi
	  * @return id produktu/uslugi
	  */
	 public String generateItemId(){
		 itemIdCounter++;
		 String itemId = Integer.toString(itemIdCounter-1);
		 String formattedItemId = String.format("%4s", itemId).replace(' ', '0');
		 return formattedItemId;
		 
	 }
	 
}
