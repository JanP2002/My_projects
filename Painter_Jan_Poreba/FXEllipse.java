import javafx.geometry.Bounds;
import java.util.ArrayList;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.input.MouseEvent;
import javafx.scene.input.ScrollEvent;
import javafx.scene.shape.Ellipse;
import javafx.scene.paint.Color;
import javafx.scene.transform.Rotate; 

/**
 * klasa definiujaca elipse
 */
public class FXEllipse extends Ellipse{
        
    private boolean active=false;
    /**
     * Konstruktor klasy FXEllipse
     * @param x Wspolrzedna x srodka elipsy
     * @param y Wspolrzedna y srodka elipsy
     * @param width Szerokosc elipsy
     * @param height Wysokosc elipsy
     * @param circleList Lista okregow na panelu (grupie) w klasie Painter
     * @param rectList Lista prostokatow na panelu (grupie) w klasie Painter
     * @param triangleList Lista trojkatow na panelu (grupie) w klasie Painter
     * @see Painter
     */
    public FXEllipse(double x, double y, double width, double height, ArrayList<FXEllipse> circleList, ArrayList<FXRectangle> rectList, ArrayList<FXTriangle> triangleList) {
        super(x, y, width, height);
        setOnMouseClicked(new FXEllipseEventHandler(circleList, rectList, triangleList));
        setOnMouseDragged(new FXEllipseEventHandler(circleList, rectList, triangleList));
        setOnScroll(new FXEllipseScrollHandler());
  
    }
  

    /**
     * 
     * @return informacja czy elipsa jest aktywna
     */
    public boolean isActive()
     {
       return active;
     }
     /**
      * Funcka sluzaca do ustawiania elipsy jak aktywnej, badz nieaktywnej
      * @param active informacja czy mamy ustawic elipse jako aktywna -true, badz nieaktywna -false
      */
     
     public void setActive(boolean active){
        this.active = active;
     }
  
    /**
     * Metoda sprawdza czy najechalismy na figure
     * @param x Wspolrzedna x punktu kliknietego
     * @param y Wspolrzedna y punktu kliknietego
     * @return Informacja czy kilkniety punkt znajduje sie wewnatrz, czy na zewnatrz elipsy
     */
    public boolean isHit(double x, double y) { 
       return getBoundsInLocal().contains(x,y);   
  
    }
  
    
    /**
     * Metoda przesuwa wspolrzedna x srodka elipsy
     * @param x wartosc o jako chcemy przesunac wspolrzedna x srodka elipsy w pikselach
     */
    public void addX(double x) {  
        this.setCenterX(this.getCenterX() +x);
    }
  
    /**
     * Metoda przesuwa wspolrzedna y srodka elipsy
     * @param y wartosc o jako chcemy przesunac wspolrzedna y srodka elipsy w pikselach
     */
    public void addY(double y) {         
      this.setCenterY(this.getCenterY() +y);
    }
  
    /**
     * Metoda zwieksza szerokosc elipsy
     * @param w wartosc o jaka chcemy zwiekszyc (jak ujemna to zmniejszyc) szerokosc elipsy
     */
    public void addWidth(double w) {    
      this.setRadiusX(this.getRadiusX()+w);
    }
  
    /**
     * Metoda zwieksza wysokosc elipsy
     * @param h wartosc o jaka chcemy zwiekszyc (jak ujemna to zmniejszyc) wysokosc elipsy
     */
    public void addHeight(double h) {     
      this.setRadiusY(this.getRadiusY()+h);
    }

    /**
     * klasa odpowiedzialna za obracanie elipsy
     * @param angle kat obrotu w stopniach
     */
    public void doRotate(double angle){
      Rotate rotate = new Rotate();
      rotate.setPivotX(getCenterX());
      rotate.setPivotY(getCenterY());
      rotate.setAngle(angle);
      getTransforms().addAll(rotate); 
    }

 // Implementacja scrollowania   
class FXEllipseScrollHandler implements EventHandler<ScrollEvent>{

    FXEllipse ellipse;

    private void doScale(ScrollEvent e) {
              
    double x = e.getX();
    double y = e.getY();
  
    // Jesli nacisnelismy na elipse
    if (ellipse.isHit(x, y)) {                 
            ellipse.addWidth(e.getDeltaY()*0.2);
            ellipse.addHeight(e.getDeltaY()*0.2);
        }
    }            
  
    @Override
    public void handle(ScrollEvent event) {
      
      ellipse = (FXEllipse) event.getSource();
      if (event.getEventType()==ScrollEvent.SCROLL && ellipse.isActive() == true){
        doScale(event);
      }
    }
  }
  
  
  // Implementacja przesuwania
  class FXEllipseEventHandler implements EventHandler<MouseEvent>{
    
    FXEllipse ellipse;
    private double x;
    private double y;
    ArrayList<FXEllipse> circleList;
    ArrayList<FXRectangle> rectList;
    ArrayList<FXTriangle> triangleList;

    FXEllipseEventHandler(ArrayList<FXEllipse> circleList, ArrayList<FXRectangle> rectList, ArrayList<FXTriangle> triangleList){
        this.circleList=circleList;
        this.rectList=rectList;
        this.triangleList=triangleList;
    }

  
    private void doMove(MouseEvent event) {
              
      double dx = event.getX() - x;
      double dy = event.getY() - y;
  
        // Jesli nacisnelismy na elipse
      if (ellipse.isHit(x, y)) {
          ellipse.addX(dx);
          ellipse.addY(dy);
        }
      x += dx;
      y += dy;            
    }
  
    
    @Override
    public void handle(MouseEvent event) {
      ellipse = (FXEllipse) event.getSource();
      for(FXEllipse circle: circleList){
        circle.setActive(false);
        circle.setStroke(circle.getFill());
        circle.setStrokeWidth(Painter.STROKE_WIDTH);
      }
      for(FXRectangle rectangle: rectList){
        rectangle.setActive(false);
        rectangle.setStroke(rectangle.getFill());
        rectangle.setStrokeWidth(Painter.STROKE_WIDTH);
      }
      for(FXTriangle triangle: triangleList){
        triangle.setActive(false);
        triangle.setStroke(triangle.getFill());
        triangle.setStrokeWidth(Painter.STROKE_WIDTH);
      }
      ellipse.setActive(true);
      ellipse.setStroke(Color.RED);
      ellipse.setStrokeWidth(Painter.STROKE_WIDTH);
      if (event.getEventType()==MouseEvent.MOUSE_CLICKED){
        x = event.getX();
        y = event.getY();
      }
      if (event.getEventType()==MouseEvent.MOUSE_DRAGGED){
        doMove(event);
      }
  
    }
  }
  

  }