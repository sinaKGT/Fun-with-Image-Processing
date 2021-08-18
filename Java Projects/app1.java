public class app1{
    public static void main(String[] args){
        /**
         * 1 2 3
         * 2 4 6
         * 3 6 9
         */
        int satr, soton;
        for(satr=1; satr<11; satr++){
            for(soton=1; soton<11; soton++){
                System.out.print(satr*soton);
                System.out.print("\t");
            }
            System.out.println();
        }
        
    }

}