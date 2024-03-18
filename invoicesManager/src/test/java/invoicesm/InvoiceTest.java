package invoicesm;

import org.junit.runner.RunWith;
import org.junit.runners.Suite;
import org.junit.runners.Suite.SuiteClasses;


/**
 * Komplet testow jednostkowych
 * klasy Invoice
 * @author Jan Poreba
 *
 */
@RunWith(Suite.class)
@SuiteClasses({ InvoiceCreationTest.class, TestCountingFullCost.class })
public class InvoiceTest {

}
