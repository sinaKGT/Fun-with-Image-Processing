import java.util.Scanner;
public class app5 {
    String loghat[] = {"USB", "VB", "VGA", "HDD"};
    String kamel[] = {"Universal Serial Bus",
                        "Visual Basic",
                        " Video Graphics Array",
                        "Hard Disk Drive"
                    };
    Scanner input = new Scanner(System.in);
    String word;
    public void fullword(){
        System.out.println("Please Enter the word: ");
        word = input.nextLine();
        int count = 0;
        int i;
        for(i=0; i<loghat.length; i++)
            if(word.compareToIgnoreCase(loghat[i]) == 0){
                System.out.println(kamel[i]);
            }else{
                count++;
            }
        if(count == loghat.length)
            System.out.println("Wor is not found");
    }
    public static void main(String[] args){
        app5 m = new app5();
        m.fullword();
    }

}
