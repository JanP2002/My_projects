import java.util.ArrayList;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.control.Menu;
import javafx.scene.control.MenuBar;
import javafx.scene.control.MenuItem;
import javafx.scene.layout.BorderPane;
import javafx.scene.Group;
import javafx.stage.Stage;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.control.SeparatorMenuItem;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;
import javafx.scene.input.MouseEvent;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.layout.Pane;
import javafx.scene.control.Dialog;
import javafx.scene.control.ButtonType;
import javafx.scene.control.ButtonBar.ButtonData;
import javafx.scene.control.TextField;
import javafx.scene.control.TextInputDialog;
import javafx.stage.Modality;
import javafx.scene.control.Button;
import javafx.scene.layout.GridPane;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.ScrollBar;
import javafx.scene.layout.VBox;
import javafx.geometry.Orientation;
import javafx.scene.control.TextArea;
import javafx.scene.control.ContextMenu;
import javafx.scene.control.MenuItem;
import javafx.scene.input.ContextMenuEvent;
import javafx.scene.control.ColorPicker;



class PanelHandler implements EventHandler<MouseEvent>{
    private double cursorX;
    private double cursorY;
    @Override
    public void handle(MouseEvent event) {
        cursorX=event.getX();
        cursorY=event.getY();
    }
}

/**
 * klasa definiujaca okno aplikacji Painter
 * @author Jan Poreba
 */

public class Painter extends Application {

    private static final int Width=500;
    private static final int Height=500;
    private static final int InfoDialogWidth = Width*2/3;
    private static final int InfoDialogHeight = Height*2/3;
    private static final int RotateDialogWidth = Width*1/2;
    private static final int RotateDialogHeight = Height*1/2;
    private static final int InfoTextWidth = InfoDialogWidth;
    private static final int InfoTextHeight = InfoDialogHeight - 40;
    private static final String ProgramTitleTxt="Painter";
    private static final String DialogTitleTxt="Painter Info";
    private static final String InfoTxt="Info";
    private static final String RotateDialogTitleTxt= "Obracanie figury";
    private static final String MenuFigureTxt="Figura";
    private static final String CircleTxt="Okrag";
    private static final String RectTxt="Prosotkat";
    private static final String TriangleTxt="Trojkat";
    private static final String ContextMenuColorText = "Zmien kolor";
    private static final String ContextMenuRotateText = "Obroc";
    private static final String RotateInstruction = "Podaj kat";
    private static final String RotateErrorText = "Nieprawidlowy kat";

    
    private static final int DefaultSize=50;
    /**
     * stala statyczna okreslajaca szerokosc obramowania wystepujacego po aktywowaniu figury
     */
    public static final int STROKE_WIDTH=3;
    /**
     * stala statyczna okreslajaca minimalne wymiary prostokata
     */
    public static final int EPSILON=10;
    private static final String DescriptionTxt=" -prosty edytor garficzny  ";
    private static final String AuthorTxt="Autor: Jan Poreba\n";
    private static final String InstructionTxt = "Instrukcja:\n\n" +
    "1. Kliknij na menubarze przycisk figura, " +
    "a nastepnie wybierz z menu jedna z figur: okrag, prostokat lub trojkat w celu narysowania wybranej figury na panelu.\n\n" +
    "2. Na panelu mozesz narysowac wiele figur.\n\n" +
    "3. W celu oznaczenia figury jako aktywnej kilknij na nia lewym przyciskiem myszy.\n" +
    "Wowczas obramowanie figury zmieni kolor na czerwony.\n\n" +
    "4. Jezeli figura jest oznaczona jako aktywna, mozesz przesunac ja w inne miejsce lub zmienic jej rozmiar za pomoca scrolla.\n\n" +
    "5. Aby przesunac aktywna figure w inne miejsce przeciagnij kursor myszy w wybrane miejsce, caly czas trzymajac nacisniety lewy przycisk myszy.\n\n" +
    "6. Aby zmienic rozmiar aktywnej figury najedz kursorem myszy na punkt znajdujacy sie wewnatrz wybranej figury, a nastepnie krec kolkiem myszy.\n\n" +
    "7. W celu zwiekszenia figury krec kolkiem myszy w gore, a w celu zmniejszenia w dol.\n\n" +
    "8. Wymiary prostokata mozna dodatkowo zmieniac, zmieniajac wspolrzedne punktu z lewego gornego rogu lub punktu z prawego dolnego rogu.\n" +
    "W tym celu kilknij na wybrany punkt lewym  przyciskiem myszy, a nastepnie przeciagnij kursor myszy w wybrane miejsce, " +
    "caly czas trzymajac nacisniety lewy przycisk myszy.\n\n" +
    "9. Wymiary trojkata mozesz dodatkowo zmienic, zamieniajc wspolrzedne wybranego z jego punktow.\n" +
    "W tym celu kilknij na wybrany punkt lewym  przyciskiem myszy, a nastepnie przeciagnij kursor myszy w wybrane miejsce, " +
    "caly czas trzymajac nacisniety lewy przycisk myszy.\n\n" +
    "10. W celu zmiany koloru figury kilknij na nia prawym przyciskiem myszy, " +
    "a nastepnie kliknij na menu kontekstowym przycisk do zmiany kolorow i wybierz kolor.\n\n" +
    "11. W celu obrocenia figury kilknij na nia prawym przyciskiem myszy, a nastepnie kilknij na menu kontekstowym przycisk obroc. " +
    "Uruchomi sie okno dialogowe. Wpisz w polu tekstowym kat obrotu, a nastepnie kilknij przycisk ok w celu wykonania obrotu.\n\n";
    private Pane group;
    private Stage dialog;
    private Stage rotateDialog;
    private ContextMenu contextMenu;
    private ColorPicker colorsPicker;

    private ArrayList<FXEllipse> circleList;
    private ArrayList<FXRectangle> rectList;
    private ArrayList<FXTriangle> triangleList;
    private static final int listsSize=128;

    /**
     * glowna metoda klasy Painter inicjujaca okno aplikacji
     * @param stage glowny kontener
     */
    @Override
    public void start(Stage stage) {

        initUI(stage,createMenuActionHandler());
        initInfoDialog();
        initRotateDialog();
        initContextMenus(createContextMenuHandler());
        
       
       
    }


    private void initUI(Stage stage, EventHandler<ActionEvent> evnHandler){
    
        stage=new Stage();
        BorderPane root = new BorderPane();
        
        group = new Pane();
        MenuBar myMenuBar = new MenuBar();
        Menu figures = new Menu(MenuFigureTxt);
        Menu info=new Menu(InfoTxt);

        
        root.setTop(myMenuBar);
        root.setCenter(group);

        circleList=new ArrayList<>(listsSize);
        rectList=new ArrayList<>(listsSize);
        triangleList=new ArrayList<>(listsSize);
        
       
        
        MenuItem  i1 = new MenuItem(CircleTxt);
        i1.setOnAction(evnHandler);
        MenuItem  i2 = new MenuItem(RectTxt);
        i2.setOnAction(evnHandler);
        MenuItem i3 = new MenuItem(TriangleTxt);
        i3.setOnAction(evnHandler);
        MenuItem i4 = new MenuItem(InfoTxt);
        i4.setOnAction(evnHandler);
        figures.getItems().addAll(i1,i2,i3);
        info.getItems().addAll(i4);
        myMenuBar.getMenus().addAll(figures,info);


        


        Scene scene = new Scene(root, Width, Height, Color.WHITESMOKE);
        stage.setTitle(ProgramTitleTxt);
        stage.setScene(scene);
        stage.sizeToScene();
        stage.show();
       
    }

    
private void initInfoDialog(){
    dialog = new Stage();
    VBox vBox= new VBox();
    Group dialogRoot = new Group(vBox);
    Scene dialogScene = new Scene(dialogRoot, InfoDialogWidth, InfoDialogHeight);
    dialog.setTitle(DialogTitleTxt);
    dialog.initModality(Modality.APPLICATION_MODAL);
    TextArea information = new TextArea(ProgramTitleTxt + DescriptionTxt + AuthorTxt + "\n" + InstructionTxt);
    information.setPrefWidth(InfoTextWidth);
    information.setPrefHeight(InfoTextHeight);
    information.setWrapText(true);
    information.setEditable(false);
    EventHandler<ActionEvent> dialogHandlerObj=new EventHandler<ActionEvent>() {
        @Override
        public void handle(ActionEvent event) {
            dialog.close();
        }
    };
    Button button = new Button("Ok");
    
    button.setOnAction(dialogHandlerObj);
    vBox.getChildren().addAll(information, button);
    dialog.setResizable(false);
    dialog.setScene(dialogScene);
    dialog.show();
    dialog.close();

    
}


private void initRotateDialog(){
    rotateDialog = new Stage();
    VBox vBox = new VBox();
    Group dialogRoot = new Group(vBox);
    Scene dialogScene = new Scene(dialogRoot, RotateDialogWidth, RotateDialogHeight);
    rotateDialog.setTitle(RotateDialogTitleTxt);
    rotateDialog.initModality(Modality.APPLICATION_MODAL);
    Label rotateInstruction = new Label(RotateInstruction);
    TextField rotateField = new TextField();
    Label rotateError = new Label();
    EventHandler<ActionEvent> dialogHandlerObj=new EventHandler<ActionEvent>() {
        @Override
        public void handle(ActionEvent event) {
            try{
                double angle = Double.parseDouble(rotateField.getText());
                rotateActiveFigure(angle);
                rotateDialog.close();
                rotateField.setText("");
                rotateError.setText("");
            }
            catch(NumberFormatException ex){
                rotateError.setText(RotateErrorText);
            }
            
        }
    };
    Button button = new Button("Ok");
    
    button.setOnAction(dialogHandlerObj);
    vBox.getChildren().addAll(rotateInstruction, rotateField, button, rotateError);
    rotateDialog.setResizable(false);
    rotateDialog.setScene(dialogScene);
    rotateDialog.show();
    rotateDialog.close();
}



private void initContextMenus(EventHandler<ActionEvent> evnHandler){
    contextMenu = new ContextMenu();
    colorsPicker = new ColorPicker();
    MenuItem itemChangeColor = new MenuItem(ContextMenuColorText, colorsPicker);
    itemChangeColor.setOnAction(evnHandler);
    MenuItem itemRotate = new MenuItem(ContextMenuRotateText);
    itemRotate.setOnAction(evnHandler);
    contextMenu.getItems().addAll(itemChangeColor, itemRotate);
    
}






    private EventHandler<ActionEvent> createMenuActionHandler(){
        EventHandler<ActionEvent> evnHandler = new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
                MenuItem m = (MenuItem) event.getSource();      
                     
                switch(m.getText()){
                    case CircleTxt:
                        FXEllipse circle=new FXEllipse(Width/2, Height/2, DefaultSize, DefaultSize, circleList, rectList, triangleList);
                        circleList.add(circle);
                        group.getChildren().add(circle);
                        circle.setOnContextMenuRequested(new EventHandler<ContextMenuEvent>() {
    
                            @Override
                            public void handle(ContextMenuEvent event) {
                
                                contextMenu.show(circle, event.getScreenX(), event.getScreenY());
                            }
                        });

                        break;
                    case RectTxt:
                        FXRectangle rectangle = new FXRectangle(Width/2, Height/2, DefaultSize, DefaultSize, circleList, rectList, triangleList);
                        rectList.add(rectangle);
                        group.getChildren().add(rectangle);
                        rectangle.setOnContextMenuRequested(new EventHandler<ContextMenuEvent>() {
    
                            @Override
                            public void handle(ContextMenuEvent event) {
                
                                contextMenu.show(rectangle, event.getScreenX(), event.getScreenY());
                            }
                        });
                        break;
                    case TriangleTxt:
                        FXTriangle triangle = new FXTriangle(circleList, rectList, triangleList, 100, 100, 200, 200, 100, 200);
                        triangleList.add(triangle);
                        group.getChildren().add(triangle);
                        triangle.setOnContextMenuRequested(new EventHandler<ContextMenuEvent>() {
    
                            @Override
                            public void handle(ContextMenuEvent event) {
                
                                contextMenu.show(triangle, event.getScreenX(), event.getScreenY());
                            }
                        });
                        break;
                    case InfoTxt:
                        dialog.showAndWait();
                        break;

                }
            }
        };
        return evnHandler;

    }

    private EventHandler<ActionEvent> createContextMenuHandler(){
        EventHandler<ActionEvent> evnHandler = new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event){
                MenuItem m = (MenuItem) event.getSource(); 
                switch(m.getText()){
                    case ContextMenuColorText:
                        fillActiveFigure();
                        break;
                    case ContextMenuRotateText:
                        rotateDialog.showAndWait();
                        break;
                }
            }

        };
        return evnHandler;
    }



    private FXEllipse getActiveCircle(){
        for(FXEllipse circle: circleList){
            if(circle.isActive()) return circle;
        }
        return null;
    }

    private FXRectangle getActiveRectangle(){
        for(FXRectangle rectangle: rectList){
            if(rectangle.isActive()) return rectangle;
        }
        return null;
    }

    private FXTriangle getActiveTriangle(){
        for(FXTriangle triangle: triangleList){
            if(triangle.isActive()) return triangle;
        }
        return null;
    }
    
    private void rotateActiveFigure(double angle){
        FXEllipse circle= getActiveCircle();
        FXRectangle rectangle = getActiveRectangle();
        FXTriangle triangle = getActiveTriangle();
        if(circle != null){
            circle.doRotate(angle);
        }
        else if(rectangle != null){
            rectangle.doRotate(angle);
        }
        else if(triangle != null){
            triangle.doRotate(angle);
        }
    }


    private void fillActiveFigure(){
        FXEllipse circle = getActiveCircle();
        FXRectangle rectangle = getActiveRectangle();
        FXTriangle triangle = getActiveTriangle();
        Color c = colorsPicker.getValue();
        if(circle != null){
            circle.setFill(c);
        }
        else if(rectangle != null){
            rectangle.setFill(c);
        }
        else if(triangle != null){
            triangle.setFill(c);
        }
    }



/**
 * Glowna funkcja testujaca klase Painter
 * @param args
 */


    public static void main(String[] args) {
        launch(args);

    }

}
