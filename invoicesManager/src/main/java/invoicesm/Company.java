package invoicesm;



/**
 * Klasa reprezentujaca firme
 * @author Jan Poreba
 *
 */
public class Company {
	/**
	 * Id firmy, dla polskich firm NIP
	 */
	private String companyId;
	/**
	 * Nazwa firmy
	 */
	private String companyName;
	/**
	 * Adress Firmy
	 */
	private String address;
	
	/**
	 * Konstruktor klasy company
	 * @param companyId id firmy
	 * @param companyName nazwa firmy
	 * @param address adres firmy
	 * @throws InvalidCompanyException wyjatek
	 *  w przypadku niepoprawnych danych firmy
	 */
	public Company(String companyId, String companyName, String address) 
			throws InvalidCompanyException {
		if(companyId.equals("")) {
			throw new InvalidCompanyException("Nie podano id firmy");
		}
		
		if(companyName.equals("")) {
			throw new InvalidCompanyException("Nie podano nazwy firmy");
		}
		
		if(address.equals("")) {
			throw new InvalidCompanyException("Nie podano adresu firmy");
		}
		
		this.companyId = companyId;
		this.companyName = companyName;
		this.address = address;
	}
	
	/**
	 * @return id firmy
	 */
	public String getCompanyId() {
		return companyId;
	}
	/**
	 * @return adres
	 */
	public String getAddress() {
		return address;
	}
	/**
	 * @param id firmy 
	 * @throws InvalidCompanyException 
	 * wyjatek
	 *  w przypadku niepoprawnych danych firmy
	 */
	public void setCompanyId(String nip) throws InvalidCompanyException {
		if(nip.equals("")) {
			throw new InvalidCompanyException("Nie podano id firmy");
		}
		this.companyId = nip;
	}
	/**
	 * @param adres firmy
	 * @throws InvalidCompanyException wyjatek
	 *  w przypadku niepoprawnych danych firmy
	 */
	public void setAddress(String address) throws InvalidCompanyException {

		if(address.equals("")) {
			throw new InvalidCompanyException("Nie podano adresu firmy");
		}
		this.address = address;
	}

	/**
	 * @return nazwa firmy
	 */
	public String getCompanyName() {
		return companyName;
	}

	/**
	 * @param nazwa firmy
	 * @throws InvalidCompanyException wyjatek
	 *  w przypadku niepoprawnych danych firmy
	 */
	public void setCompanyName(String companyName) throws InvalidCompanyException {
		if(companyName.equals("")) {
			throw new InvalidCompanyException("Nie podano nazwy firmy");
		}
		this.companyName = companyName;
	}
	

}