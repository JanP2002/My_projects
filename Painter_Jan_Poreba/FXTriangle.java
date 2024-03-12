import javafx.geometry.Bounds;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.input.MouseEvent;
import javafx.scene.input.ScrollEvent;
import javafx.scene.paint.Color;
import java.util.ArrayList;
import java.lang.*;
import javafx.scene.shape.*;
import javafx.collections.*;
import javafx.scene.transform.*; 

/**
 * Klasa definiujaca trojkat
 */
public class FXTriangle extends Polygon {

  private boolean active;
  private double centerX;
  private double centerY;


  /**
   * Konstruktor klasy FXTriangle
   * @param circleList Lista okregow na panelu (grupie) w klasie Painter
   * @param rectList Lista prostokatow na panelu (grupie) w klasie Painter
   * @param triangleList Lista trojkatow na panelu (grupie) w klasie Painter
   * @param points Tablica wspolrzednych wierzcholkow trojkata
   * @see Painter
   */  
  public FXTriangle(ArrayList<FXEllipse> circleList, ArrayList<FXRectangle> rectList, ArrayList<FXTriangle> triangleList, double... points) { 
        
        super(points);
        active=false;
        centerX = (points[0] + points[2] + points[4])/3.0;
        centerY = (points[1]+ points[3] + points[5])/3.0;
      
        FXTriangleEventHandler handleObject= new FXTriangleEventHandler(circleList, rectList, triangleList);
        setOnMouseClicked(handleObject);
        setOnMouseDragged(handleObject);
        setOnMousePressed(handleObject);
        setOnScroll(new FXTriangleScrollHandler());
  }
/**
 * Metoda zwracajaca wspolrzedna x srodka trojkata
 * @return Wspolrzedna x srodka trojkata
 */
  public double getCenterX()
  {
    return centerX;
  }
/**
 * Metoda zwracajaca wspolrzedna y srodka trojkata
 * @return Wspolrzedna y srodka trojkata
 */
  public double getCenterY(){
    return centerY;
  }

/**
 * Metoda przesuwajaca srodek trojkata
 * @param x wspolrzedna x o jako srodek trojkata ma byc przesuniety
 * @param y wspolrzedna y o jako srodek trojkata ma byc przesuniety
 */
  public void translateCenter(double x, double y){
    centerX+=x;
    centerY+=y;
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
     * Metoda sluzaca do ustawiania trojkata jak aktywnego, badz nieaktywnego
     * @param active informacja czy mamy ustawic trojkat jako aktywny -true, badz nieaktywny -false
     */
     public void setActive(boolean active){
        this.active = active;
     }
    /**
     * Metoda sprawdza czy najechalismy na figure
     * @param x Wspolrzedna x punktu kliknietego
     * @param y Wspolrzedna y punktu kliknietego
     * @return Informacja czy kilkniety punkt znajduje sie wewnatrz, czy na zewnatrz trojkata
     */
    public boolean isHit(double x, double y) { 
        return getBoundsInLocal().contains(x,y);   
    }

    
    /**
     * Klasa odpowiadajaca za obracanie trojkata
     * @param angle kat obrotu w stopniach
     */
    public void doRotate(double angle){
      Rotate rotate = new Rotate();
      rotate.setPivotX(centerX);
      rotate.setPivotY(centerY);
      rotate.setAngle(angle);
      getTransforms().addAll(rotate); 
    }
    



    // Implementacja przesuwania
  class FXTriangleEventHandler implements EventHandler<MouseEvent>{
    
    FXTriangle triangle;
    private double x;
    private double y;
    private double epsilon;
    private int cornerIdx;
    ArrayList<FXEllipse> circleList;
    ArrayList<FXRectangle> rectList;
    ArrayList<FXTriangle> triangleList;


    FXTriangleEventHandler(ArrayList<FXEllipse> circleList, ArrayList<FXRectangle> rectList, ArrayList<FXTriangle> triangleList){
      this.circleList=circleList;
      this.rectList=rectList;
      this.triangleList=triangleList;
      epsilon = Painter.EPSILON;
      cornerIdx=-1;//-1 na zwentarz, 0 pierwszy pierzcholek, 1 drugi wierzcholek, 2 trzeci wierzcholek, 3 wnetrze
  }
  
    private void doMove(MouseEvent event) {
              
      double dx = event.getX() - x;
      double dy = event.getY() - y;
  
       if (triangle.isHit(x, y)) {
        ObservableList<Double> pointsList  = triangle.getPoints();
        double[] points=new double[6];
        for(int i=0;i<6;i++){
          points[i]=pointsList.get(i);
        }
        pointsList.remove(0,6);
        for(int i=0;i<6;i++){
          if(i%2 ==0) pointsList.addAll(points[i]+dx);
          else pointsList.addAll(points[i]+dy);
        }
        translateCenter(dx, dy);

      }
      x += dx;
      y += dy;            
    }
  

    
 private void setPressedCorner(FXTriangle Triangle, MouseEvent event){
  ObservableList<Double> points  = triangle.getPoints();

  if(Math.abs(event.getX()-points.get(0))<epsilon && Math.abs(event.getY()-points.get(1))<epsilon){
     cornerIdx=0;
   }
  else if(Math.abs(event.getX()-points.get(2))<epsilon && Math.abs(event.getY()-points.get(3))<epsilon){
    cornerIdx=1;
  }
  else if(Math.abs(event.getX()-points.get(4))<epsilon && Math.abs(event.getY()-points.get(5))<epsilon){
    cornerIdx=2;
  }
  else{
    cornerIdx=3;
  }
   
 }
    
  


  private void doResize(MouseEvent event) {

    triangle.getPoints().remove(2*cornerIdx,2*cornerIdx+2);
    triangle.getPoints().addAll(event.getX(),event.getY());
    cornerIdx=2;

  }

    @Override
    public void handle(MouseEvent event) {
  
      triangle = (FXTriangle) event.getSource();
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
      for(FXTriangle triang: triangleList){ //konflikt oznaczen z triangle
        triang.setActive(false);
        triang.setStroke(triang.getFill());
        triang.setStrokeWidth(Painter.STROKE_WIDTH);
      }
      triangle.setActive(true);
      triangle.setStroke(Color.RED);
      triangle.setStrokeWidth(Painter.STROKE_WIDTH);
      
  
      if (event.getEventType()==MouseEvent.MOUSE_CLICKED || event.getEventType()==MouseEvent.MOUSE_PRESSED){
        x = event.getX();
        y = event.getY();
      }
      if(event.getEventType()==MouseEvent.MOUSE_PRESSED)
      {
        setPressedCorner(triangle, event);
      }
      
      
      if (event.getEventType()==MouseEvent.MOUSE_DRAGGED){
        if(cornerIdx==0 || cornerIdx==1 || cornerIdx==2){
          doResize(event);
        }
        else if(cornerIdx==3){
          doMove(event);
        }
      }
        
      
  
    }
  }

  // Implementacja scrollowania   
class FXTriangleScrollHandler implements EventHandler<ScrollEvent>{

    FXTriangle triangle;

    private void doScale(ScrollEvent e) {
              
    double x = e.getX();
    double y = e.getY();
  
    // Jesli nacisnelismy na trojkat
    if (triangle.isHit(x, y)) {                 
      Scale scale = new Scale();
      
      scale.setX(1+e.getDeltaY()*0.001);
      scale.setY(1+e.getDeltaY()*0.001);
      scale.setPivotX(triangle.getCenterX());
      scale.setPivotY(triangle.getCenterY());
      triangle.getTransforms().add(scale);
    }
  }            
  
    @Override
    public void handle(ScrollEvent event) {
      
      triangle = (FXTriangle) event.getSource();
      if (event.getEventType()==ScrollEvent.SCROLL  && triangle.isActive() == true){
        doScale(event);
      }
    }
  }
}