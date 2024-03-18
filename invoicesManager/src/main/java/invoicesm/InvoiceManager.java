package invoicesm;

import java.util.LinkedList;
import java.util.List;
import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.geometry.Pos;
import javafx.geometry.VPos;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.Alert.AlertType;
import javafx.scene.control.Button;
import javafx.scene.control.DatePicker;
import javafx.scene.control.Label;
import javafx.scene.control.ListView;
import javafx.scene.control.Separator;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.stage.Modality;
import javafx.stage.Stage;

/**
 * GUI aplikacji do zarzadzania fakturami
 * @author Jan Poreba
 */
public class InvoiceManager extends Application{

	/**
	 * okno aplikacji obslugujace
	 * wystawianie nowej faktury
	 */
	private Stage creatingInvoiceStage;
	/**
	 * glowne okno aplikacji z
	 * poziomu, ktorego mozemy wyswietlac
	 * liste faktur oraz zlecac dodanie, czy wyswietlenie
	 * faktury
	 */
	private Stage invoiceListStage;
	/**
	 * lista pozycji na fakturze
	*/
	private List<Order> orderList;
	/**
	 * lista pozycji na fakturze
	 * w innym formacie
	 */
	private ObservableList<OrderView> ordersData =
            FXCollections.observableArrayList();
	/**
	 * okno do wyswietlania
	 * faktury
	 */
	private Stage invoiceDisplayDialog;
	/**
	 * obiekt odpowiedzialny za
	 * prezenatcje faktury
	 */
	private InvoicePresentationIF invoicePresenter;
	/**
	 * tabela pozycji na wystawianej fakturze
	 */
	private ListView<String> invoiceListView;
	/**
	 * obiekt logiki biznesowej,
	 * na podstawie polecen z aplikacji
	 * wywoluje metody wykonujace
	 * operacje na bazie danych
	 */
	private BusinessLogic businessLogic;
	/**
	 * przycisk dodania nowej faktury
	 */
	private Button newInvoiceButton;
	/**
	 * przycisk wyswietlania faktury
	 */
	private Button displayInvoiceButton;
	/**
	 * przycisk wylogowania z systemu
	 */
	private Button closingInvoiceListButton;
	
	
	
	
	
	
	
	
	/**
	 * metoda tworzaca glowne okno aplikacji,
	 * wyswietlajace liste faktur
	 */
	private void initInvoiceListWindow() {
		invoiceListStage = new Stage();
    	invoiceListStage.setTitle(Config.INVOICE_MANAGER_TITLE);
    	
	    
    	invoiceListView = new ListView<>();
    	
    
		List<Invoice> invoiceList = 
			businessLogic.readInvoiceList();
		
		
		List<String> invoiceLabelsList =
				invoicePresenter.generateInvoiceLabelList(invoiceList);
				
		
    	
    	VBox vBox= new VBox();
    	ObservableList<String> invoicesLabelsObsrvable =FXCollections.observableArrayList(invoiceLabelsList);
    	invoiceListView.setItems(invoicesLabelsObsrvable);
		invoiceListView.setPrefWidth(Config.WIDTH);
    	
    	
		
    	HBox listHBox = new HBox(invoiceListView);
    	listHBox.setAlignment(Pos.CENTER);
    	listHBox.setSpacing(Config.GAP);
    	
    	
    	newInvoiceButton = new Button(Config.NEW_INVOICE_BUTTON_TXT);
    	displayInvoiceButton = new Button(Config.DISPLAY_INVOICE_BUTTON_TXT);
    	HBox buttonsHBox = new HBox(newInvoiceButton, displayInvoiceButton);
    	buttonsHBox.setAlignment(Pos.CENTER);
    	buttonsHBox.setSpacing(Config.GAP);
    	
    	Label errorLabel = new Label();
    	errorLabel.setTextFill(Color.color(1, 0, 0));
    	HBox errorLabelHBox = new HBox(errorLabel);
    	errorLabelHBox.setAlignment(Pos.CENTER);
    	errorLabelHBox.setSpacing(Config.GAP);
    	
    	closingInvoiceListButton =
    			new Button(Config.SIGNING_OUT_TXT);
    	HBox closingButtonHBox = new HBox(closingInvoiceListButton);
    	closingButtonHBox.setAlignment(Pos.CENTER);
    	closingButtonHBox.setSpacing(Config.GAP);
    	
    	
    	 vBox.getChildren().addAll(listHBox, buttonsHBox, errorLabelHBox, closingButtonHBox);
    	vBox.setSpacing(Config.GAP);
    	Scene windowScene = new Scene(vBox, Config.WIDTH, Config.HEIGHT);
	    invoiceListStage.setResizable(true);
	    invoiceListStage.setScene(windowScene);
	    invoiceListStage.show();
	    
	    
	    EventHandler<ActionEvent> newInvoiceHandler = new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
            	initCreatingInvoiceWindow();
            	creatingInvoiceStage.show();
            	
            	
            	
            }
	    };
	    newInvoiceButton.setOnAction(newInvoiceHandler);
	    
	        
        EventHandler<ActionEvent> displayButtonHandler = new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {

            	int index = invoiceListView.getSelectionModel().getSelectedIndex();
            	if(index >= 0) {
            		Invoice currentInvoice =
	            			invoiceList.get(index);
            		errorLabel.setText("");
	            	initInvoiceDisplayDialog(currentInvoice);
	            	invoiceDisplayDialog.showAndWait();
            	}
            	else {
            		errorLabel.setText(Config.NO_INVOICE_CHOSEN_ERROR_TXT);
            	}

            }
	    };
	    
	    displayInvoiceButton.setOnAction(displayButtonHandler);
	    
	    
	    
	    
	    
	    
	    EventHandler<ActionEvent> closingHandler = new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
            	invoiceListStage.close();
            	

            }
	    };
	    
	    closingInvoiceListButton.setOnAction(closingHandler);
	    
		
	}
	
	
	/**
	 * Metoda odpowiedzalna za stworzenie okna
	 * tworzenia faktury 
	 */
	private void initCreatingInvoiceWindow() {
		creatingInvoiceStage = new Stage();
		creatingInvoiceStage.setTitle(Config.CREATING_INVOICE_WINDOW_TITLE);
		
		BorderPane borderPane = new BorderPane();
    	
    	GridPane gridPane = new GridPane();
    	gridPane.setHgap(Config.GAP);
    	gridPane.setVgap(Config.GAP);
    	borderPane.setTop(gridPane);
    	
    	TableView<OrderView> ordersTable = new TableView<>();
    	ordersTable.setPrefWidth(Config.WIDTH);
    	HBox tableHBox = new HBox(ordersTable);
    	tableHBox.setAlignment(Pos.CENTER);
        tableHBox.setSpacing(Config.GAP);
        Button confirmButton = new Button(Config.CONFIRM_BUTTON_TXT);
        HBox confirmButtonHBox = new HBox(confirmButton);
        confirmButtonHBox.setAlignment(Pos.CENTER);
        confirmButtonHBox.setSpacing(Config.GAP);
    	VBox centerVBox = new VBox(tableHBox, confirmButtonHBox);
    	centerVBox.setSpacing(Config.GAP);
    	borderPane.setCenter(centerVBox);
    	
    	
    	Label purchasingCompanyTitle = new Label(Config.PURCHASING_COMPANY_TITLE);
    	Label purchasingCompanyIdTitle = new Label(Config.PURCHASING_COMPANY_ID_TITLE);
    	Label purchasingCompanyAddressTitle = new Label(Config.PURCHASING_COMPANY_ADDRESS_TITLE);
    	
    	TextField purchasingCompanyIdTextField = new TextField();
    	TextField purchasingCompanyNameTextField = new TextField();
    	TextField purchasingCompanyAddressTextField = new TextField();
    	
    	
    	gridPane.add(purchasingCompanyTitle, 0, 0);
    	gridPane.add(purchasingCompanyNameTextField, 1, 0);
    	gridPane.add(purchasingCompanyIdTitle, 0, 1);
    	gridPane.add(purchasingCompanyIdTextField, 1, 1);
    	gridPane.add(purchasingCompanyAddressTitle, 0, 2);
    	gridPane.add(purchasingCompanyAddressTextField, 1, 2);
    	//gridPane.add(invoiceDate, 2, 0);
    	
    	Label sellingCompanyTitle = new Label(Config.SELLING_COMPANY_TITLE);
    	Label sellingCompanyIdTitle = new Label(Config.SELLING_COMPANY_ID_TITLE);
    	Label sellingCompanyAddressTitle = new Label(Config.SELLING_COMPANY_ADDRESS_TITLE);
    	
    	TextField sellingCompanyIdTextField = new TextField();
    	TextField sellingCompanyNameTextField = new TextField();
    	TextField sellingCompanyAddressTextField = new TextField();
    	
    	
    	
    	gridPane.add(sellingCompanyTitle, 2, 0);
    	gridPane.add(sellingCompanyNameTextField, 3, 0);
    	gridPane.add(sellingCompanyIdTitle, 2, 1);
    	gridPane.add(sellingCompanyIdTextField, 3, 1);
    	gridPane.add(sellingCompanyAddressTitle, 2, 2);
    	gridPane.add(sellingCompanyAddressTextField, 3, 2);
    	
    	
    	Label invoiceDate = new Label(Config.INVOICE_DATE_TITLE);
    	DatePicker calendar = new DatePicker();
    	
    	
    	gridPane.add(invoiceDate, 0, 3);
    	gridPane.add(calendar, 1, 3);
    	
    	Separator separator = new Separator();
        separator.setValignment(VPos.CENTER);
        GridPane.setColumnSpan(separator, 4);
    	gridPane.add(separator, 0, 4);
    	
    	
    	
    	Label itemNameTitle = new Label(Config.ITEM_NAME_TITLE);
    	Label itemPriceTitle = new Label(Config.ITEM_PRICE_TITLE);
    	Label amountTitle = new Label(Config.AMOUNT_TITLE);
    	
    	TextField itemNameTextField = new TextField();
    	TextField itemPriceTextField = new TextField();
    	TextField amountTextField = new TextField();
    	
    	gridPane.add(itemNameTitle, 0, 5);
    	gridPane.add(itemPriceTitle, 1, 5);
    	gridPane.add(amountTitle, 2, 5);
    	
    	Button addOrderButton = new Button(Config.ADD_ORDER_BUTTON_TXT);
    	
    	gridPane.add(itemNameTextField, 0, 6);
    	gridPane.add(itemPriceTextField, 1, 6);
    	gridPane.add(amountTextField, 2, 6);
    	gridPane.add(addOrderButton, 3, 6);
    	
    	
    	
    	
    	ordersTable.setEditable(true);
    	TableColumn itemNameCol = new TableColumn(Config.ITEM_NAME_COL_TXT);
    	itemNameCol.setCellValueFactory(
                 new PropertyValueFactory<OrderView, String>("itemName"));
        TableColumn itemPriceCol = new TableColumn(Config.ITEM_PRICE_COL_TXT);
        itemPriceCol.setCellValueFactory(
                new PropertyValueFactory<OrderView, Double>("itemPrice"));
        TableColumn amountCol = new TableColumn(Config.AMOUNT_COL_TXT);
        amountCol.setCellValueFactory(
                new PropertyValueFactory<OrderView, Double>("amount"));
        TableColumn patchyPriceCol = new TableColumn(Config.PATCHY_PRICE_COL_TXT);
        patchyPriceCol.setCellValueFactory(
                new PropertyValueFactory<OrderView, Double>("patchyPrice"));
        
        ordersTable.getColumns().addAll(itemNameCol, itemPriceCol, amountCol, patchyPriceCol);
        ordersData =
             FXCollections.observableArrayList();
        ordersTable.setItems(ordersData);
    	
        orderList = new LinkedList<>();
        EventHandler<ActionEvent> addingOrderHandler = new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
                Alert orderErrorAlert = new Alert(AlertType.ERROR);
                orderErrorAlert.setTitle(Config.ERROR_ALERT_TITLE);
                orderErrorAlert.initModality(Modality.APPLICATION_MODAL);
               
               
                
                try {
                	String itemName = 
                     		itemNameTextField.getText();
                    String itemPriceString =
                     		itemPriceTextField.getText();
                    double price =
                    		1.0 * Math.round(100 * Double.parseDouble(itemPriceString)) / 100.0;
                    String amountString =
                     		amountTextField.getText();
                    double amount =
                    		1.0 * Math.round(10000 * Double.parseDouble(amountString)) / 10000.0;
                    
					Order order = new Order(itemName, price, amount);
					orderList.add(order);
					
					ordersData.add(new OrderView(order));
					
					itemNameTextField.setText("");
					itemPriceTextField.setText("");
					amountTextField.setText("");
					
					
					
				} catch (NumberFormatException e) {
					orderErrorAlert.setHeaderText(Config.INVALID_ORDER_TXT);
					orderErrorAlert.show();
				} catch (InvalidOrderException | InvalidItemException  e) {
					orderErrorAlert.setHeaderText(e.getMessage());
					orderErrorAlert.show();
				}
          
            }
        };
        
        addOrderButton.setOnAction(addingOrderHandler);
        
    	 EventHandler<ActionEvent> creatingInvoiceHandler = new EventHandler<ActionEvent>() {
	            @Override
	            public void handle(ActionEvent event) {
	                Alert errorAlert = new Alert(AlertType.ERROR);
	                errorAlert.setTitle(Config.ERROR_ALERT_TITLE);
	                errorAlert.initModality(Modality.APPLICATION_MODAL);
	                String purchasingCompanyId = 
	                		purchasingCompanyIdTextField.getText();
	                String purchasingCompanyName =
	                		purchasingCompanyNameTextField.getText();
	                String purchasingCompanyAddress =
	                		purchasingCompanyAddressTextField.getText();
	                
	                String sellingCompanyId = 
	                		sellingCompanyIdTextField.getText();
	                String sellingCompanyName =
	                		sellingCompanyNameTextField.getText();
	                String sellingCompanyAddress =
	                		sellingCompanyAddressTextField.getText();
	                
	                try {
						Invoice invoice = new Invoice(purchasingCompanyId, purchasingCompanyName, purchasingCompanyAddress,
								sellingCompanyId, sellingCompanyName, sellingCompanyAddress, calendar.getValue());
						for(Order order : orderList) {
							invoice.addOrder(order);
						}
						
						businessLogic.insertInvoiceItems(orderList);
						Company sellingCompany = invoice.getSellingCompany();
						Company purchasingCompany = invoice.getPurchasingCompany();
						businessLogic.insertCompany(sellingCompany);
						businessLogic.insertCompany(purchasingCompany);
						businessLogic.insertInvoice(invoice);
						refreshInvoiceList();
						creatingInvoiceStage.close();
						
						
					} catch (InvalidCompanyException e) {
						errorAlert.setHeaderText(e.getMessage());
						errorAlert.show();
					}
	                
	                
	            	
	            }
	        };
	        
	        confirmButton.setOnAction(creatingInvoiceHandler);
    	
    	
    	
    	Scene dialogScene = new Scene(borderPane, Config.WIDTH, Config.HEIGHT);
    	creatingInvoiceStage.setResizable(true);
    	creatingInvoiceStage.setScene(dialogScene);
    	creatingInvoiceStage.show();
		
	}
	
	
	/**
	 * metoda aktualizujaca widok listy faktur
	 */
    private void refreshInvoiceList() {
    	List<Invoice> invoiceList = 
				businessLogic.readInvoiceList();
			
			
		List<String> invoiceLabelsList =
					invoicePresenter.generateInvoiceLabelList(invoiceList);
		ObservableList<String> invoicesLabelsObsrvable =FXCollections.observableArrayList(invoiceLabelsList);
    	invoiceListView.setItems(invoicesLabelsObsrvable);
    }
    /**
	 * Metoda odpowiedzialna za storzenie okna
	 * wyswietlania faktury
	 * @param invoice faktura, ktora
	 * chcemy zaprezentowac
	 */
	private void initInvoiceDisplayDialog(Invoice invoice) {
		invoiceDisplayDialog = new Stage();
    	invoiceDisplayDialog.setTitle(Config.INVOICE_DISPLAY_DIALOG_TITLE);
    	TextArea invoiceContent = new TextArea();
    	invoiceContent.setPrefHeight(Config.INVOICE_HEIGHT);
    	invoiceContent.setFont(Font.font("Consolas"));
    	String invoiceString = invoicePresenter.generateInvoiceView(invoice);
    	invoiceContent.setText(invoiceString);
    	invoiceContent.setEditable(false);
    	Button closingButton = new Button(Config.CLOSING_BUTTON_TXT);
    	HBox closingButtonHBox = new HBox(closingButton);
    	closingButtonHBox.setAlignment(Pos.CENTER);
    	closingButtonHBox.setSpacing(Config.GAP);
    	VBox vBox = new VBox(invoiceContent, closingButtonHBox);
    	Scene dialogScene = new Scene(vBox, Config.WIDTH, Config.HEIGHT);
    	invoiceDisplayDialog.setResizable(true);
    	invoiceDisplayDialog.setScene(dialogScene);
    	
    	
    	EventHandler<ActionEvent> closingHandler = new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
                invoiceDisplayDialog.close();
                
                
            	
            }
        };
        
        closingButton.setOnAction(closingHandler);
	}
	
	
	
	/**
	 * Metoda tworzaca GUI do
	 * zarzadzania fakturami
	 */
	@Override
	public void start(Stage arg0) throws Exception {
		this.invoicePresenter = new InvoicePresentation();
		this.businessLogic = new BusinessLogic();
		initInvoiceListWindow();
		
	}
	
	
	/**
	 * Glowna metoda testujaca klase InvoiceManager
	 * @param args parametry z jakimi
	 * wywolany jest program
	 */
    public static void main(String[] args) {
        launch(args);
   
    }


}
