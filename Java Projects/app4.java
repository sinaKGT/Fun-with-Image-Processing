import java.util.Scanner;

import java.util.Scanner;

public class app4 {
    Scanner input = new Scanner(System.in);
    String word =  new String();
    String abbrev = new String();
    Character c = new Character('q');
    public void findAbbreviation(){
        System.out.println("Please enter your word: ");
        word = input.nextLine();
        
        String[] str = word.split("\\s+");
        if(str.length > 1){
            int i;
            for(i=0; i< str.length; i++){
                char ch = c.toUpperCase(str[i].charAt(0));
                abbrev += ch;
            }
            System.out.println(abbrev);

        }else{
            System.out.println("Error please enter the correct word!");
        }
    }
    public static void main(String[] args)
    {
        new app4().findAbbreviation();
    }

}