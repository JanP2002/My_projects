import javafx.geometry.Bounds;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.input.MouseEvent;
import javafx.scene.input.ScrollEvent;
import javafx.scene.shape.Rectangle;
import javafx.scene.paint.Color;
import java.util.ArrayList;
import java.lang.*;
import javafx.scene.transform.Rotate; 

/**
 * Klasa definiujaca prostokat
 */
public class FXRectangle extends Rectangle {

  private boolean active=false;
    
  /**
   * Konstruktor klasy FXRectangle
   * @param x Wspolrzedna x lewego gornego rogu prostokata
   * @param y Wspolrzedna y lewego gornego rogu prostokata
   * @param width Szerokosc prostokata
   * @param height Wysokosc prostokata
   * @param circleList Lista okregow na panelu (grupie) w klasie Painter
   * @param rectList Lista prostokatow na panelu (grupie) w klasie Painter
   * @param triangleList Lista trojkatow na panelu (grupie) w klasie Painter
   * @see Painter
   */
  public FXRectangle(double x, double y, double width, double height, ArrayList<FXEllipse> circleList, ArrayList<FXRectangle> rectList, ArrayList<FXTriangle> triangleList) { 
        super(x, y, width, height);
        FXRectangleEventHandler handleObject= new FXRectangleEventHandler(circleList, rectList, triangleList);
        setOnMouseClicked(handleObject);
        setOnMouseDragged(handleObject);
        setOnMousePressed(handleObject);
        setOnScroll(new FXRectangleScrollHandler());
    }

    /**
     * Metoda zwracajaca informacje, czy prostokat jest aktywny
     * @return informacja czy prostokat jest aktywny
     */
    public boolean isActive()
     {
       return active;
     }
     /**
      * Metoda sluzaca do ustawiania prostokata jak aktywnego, badz nieaktywnego
      * @param active informacja czy mamy ustawic prostokat jako aktywny -true, badz nieaktywny -false
      */
     public void setActive(boolean active){
        this.active = active;
     }
    /**
     * Metoda sprawdza czy najechalismy na figure
     * @param x Wspolrzedna x punktu kliknietego
     * @param y Wspolrzedna y punktu kliknietego
     * @return Informacja czy kilkniety punkt znajduje sie wewnatrz, czy na zewnatrz prostokata
     */
    public boolean isHit(double x, double y) { 
        return getBoundsInLocal().contains(x,y);   
    }

    /**
     * Metoda przesuwa wspolrzedna x lewego gornego rogu prostokata
     * @param x wartosc o jako chcemy przesunac wspolrzedna x lewego gornego rogu prostokata w pikselach
     */
    public void addX(double x) {  
        setX(getX()+x);
    }

    /**
     * Metoda przesuwa wspolrzedna y lewego gornego rogu prostokata
     * @param y wartosc o jako chcemy przesunac wspolrzedna y lewego gornego rogu prostokata w pikselach
     */
    public void addY(double y) {  
        setY(getY()+y);
    }
    
    /**
     * Metoda zwieksza szerokosc prostokata
     * @param w wartosc o jaka chcemy zwiekszyc (jak ujemna to zmniejszyc) szerokosc prostokata
     */
    public void addWidth(double w) {
        setWidth(getWidth()+w);
    }
    
    /**
     * Metoda zwieksza wysokosc prostokata
     * @param h wartosc o jaka chcemy zwiekszyc (jak ujemna to zmniejszyc) wysokosc prostokata
     */
    public void addHeight(double h) {     
        setHeight(getHeight()+h);
    }

    /**
     * Matoda zwraca wspolrzedna x srodka prostokata
     * @return wspolrzedna x srodka prostokata
     */
   private double centerX(){
      return getX() + getWidth()/2;
    }

    /**
     * Matoda zwraca wspolrzedna y srodka prostokata
     * @return wspolrzedna y srodka prostokata
     */
    private double centerY(){
      return getY() + getHeight()/2.0;
    }

    /**
     * klasa enum, ktorej wartosci odpowiadaja szczegolnym obszarom prostokata
     */
    public enum ClickModeEnum{
    /**
     * wnetrze prostokata 
     */
    INTERIOR, 
    /**
     * lewy gorny rog prostokata
     */
    UPPER_LEFT,
    /**
     * prawy dolny rog prostokata
     */
    BOTTOM_RIGHT;
  }

/**
 * Klasa odpowiadajaca za obracanie prostokata
 * @param angle kat obrotu w stopniach
 */
    public void doRotate(double angle){
      Rotate rotate = new Rotate();
      rotate.setPivotX(centerX());
      rotate.setPivotY(centerY());
      rotate.setAngle(angle);
      getTransforms().addAll(rotate);  
    }

    // Implementacja przesuwania
  class FXRectangleEventHandler implements EventHandler<MouseEvent>{
    
    FXRectangle rectangle;
    private double x;
    private double y;
    ClickModeEnum clickMode;
    ArrayList<FXEllipse> circleList;
    ArrayList<FXRectangle> rectList;
    ArrayList<FXTriangle> triangleList;


    FXRectangleEventHandler(ArrayList<FXEllipse> circleList, ArrayList<FXRectangle> rectList, ArrayList<FXTriangle> triangleList){
      this.circleList=circleList;
      this.rectList=rectList;
      this.triangleList=triangleList;
      clickMode = ClickModeEnum.INTERIOR;
  }
  
    private void doMove(MouseEvent event) {
              
      double dx = event.getX() - x;
      double dy = event.getY() - y;
  
        // Jesli nacisnelismy na prostokat
       if (rectangle.isHit(x, y)) {
            rectangle.addX(dx);
            rectangle.addY(dy);
        }
      x += dx;
      y += dy;            
    }
  

    

    private boolean isBottomRight(FXRectangle rectangle, MouseEvent event){
        double bottomRightX = rectangle.getX() + rectangle.getWidth();
        double bottomRightY = rectangle.getY() + rectangle.getHeight();
        return (Math.abs(bottomRightX - event.getX()) < Painter.EPSILON && Math.abs(bottomRightY - event.getY()) < Painter.EPSILON);
    }
  
    private boolean isUpperLeft(FXRectangle rectangle, MouseEvent event){
      double UpperLeftX = rectangle.getX();
      double UpperLeftY = rectangle.getY();;
      return (Math.abs(UpperLeftX - event.getX()) < Painter.EPSILON && Math.abs(UpperLeftY - event.getY()) < Painter.EPSILON);
  }

  private void doResize(MouseEvent event) {
    if(clickMode.equals(ClickModeEnum.UPPER_LEFT)){
      double rectX = rectangle.getX();//stary prostokat
      double rectY = rectangle.getY();
      if(rectangle.getWidth()>Painter.EPSILON || rectX - event.getX()>0){
        rectangle.setX(event.getX());
        rectangle.setWidth(Math.max(rectangle.getWidth() + rectX - event.getX(),Painter.EPSILON));
      }
      if(rectangle.getHeight()>Painter.EPSILON || rectY - event.getY()>0)
      {
        rectangle.setY(event.getY());
        rectangle.setHeight(Math.max(rectangle.getHeight() + rectY - event.getY(),Painter.EPSILON));
      }
      
      
    }
    else //clickMode.equals(ClickModeEnum.BOTTOM_RIGHT)
    {
      
      rectangle.setWidth(Math.max(event.getX() - rectangle.getX(),Painter.EPSILON));
      rectangle.setHeight(Math.max(event.getY() - rectangle.getY(),Painter.EPSILON));
    }
  }

    @Override
    public void handle(MouseEvent event) {
  
      rectangle = (FXRectangle) event.getSource();
      for(FXEllipse circle: circleList){
        circle.setActive(false);
        circle.setStroke(circle.getFill());
        circle.setStrokeWidth(Painter.STROKE_WIDTH);
      }
      for(FXRectangle rect: rectList){
        rect.setActive(false);//konflikt oznaczen z rectangle
        rect.setStroke(rect.getFill());
        rect.setStrokeWidth(Painter.STROKE_WIDTH);
      }
      for(FXTriangle triangle: triangleList){
        triangle.setActive(false);
        triangle.setStroke(triangle.getFill());
        triangle.setStrokeWidth(Painter.STROKE_WIDTH);
      }
      rectangle.setActive(true);
      rectangle.setStroke(Color.RED);
      rectangle.setStrokeWidth(Painter.STROKE_WIDTH);
      
  
      if (event.getEventType()==MouseEvent.MOUSE_CLICKED || event.getEventType()==MouseEvent.MOUSE_PRESSED){
        x = event.getX();
        y = event.getY();
      }
      if(event.getEventType()==MouseEvent.MOUSE_PRESSED && isBottomRight(rectangle, event))
      {
          clickMode = ClickModeEnum.BOTTOM_RIGHT;
          
      }
      else if(event.getEventType()==MouseEvent.MOUSE_PRESSED && isUpperLeft(rectangle, event))
      {
        clickMode = ClickModeEnum.UPPER_LEFT;
      }
      else if(event.getEventType()==MouseEvent.MOUSE_PRESSED){
        clickMode = ClickModeEnum.INTERIOR;
      }
      
      
      if (event.getEventType()==MouseEvent.MOUSE_DRAGGED){
        switch (clickMode){
          case INTERIOR: 
          doMove(event);
          break;
          case UPPER_LEFT: 
          case BOTTOM_RIGHT:
          doResize(event);
          break;
        }
        
      }
  
    }
  }

  // Implementacja scrollowania   
class FXRectangleScrollHandler implements EventHandler<ScrollEvent>{

    FXRectangle rectangle;

    private void doScale(ScrollEvent e) {
              
    double x = e.getX();
    double y = e.getY();
  
    // Jesli nacisnelismy na prostokat
    if (rectangle.isHit(x, y)) {                 
            rectangle.addWidth(e.getDeltaY()*0.2);
            rectangle.addHeight(e.getDeltaY()*0.2);
        }
    }            
  
    @Override
    public void handle(ScrollEvent event) {
      
        rectangle = (FXRectangle) event.getSource();
      if (event.getEventType()==ScrollEvent.SCROLL  && rectangle.isActive() == true){
        doScale(event);
      }
    }
  }
}