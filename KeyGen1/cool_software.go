package main

import (
    "fmt"
    "os"
    "bufio"
    "strings"
    "crypto/sha256"
)

const TITLE = `
                     (                                       
   (            (    )\ )     (       )                      
   )\           )\  (()/(     )\ ) ( /((  (      ) (     (   
 (((_)  (    ( ((_)  /(_)) ( (()/( )\())\))(  ( /( )(   ))\  
 )\___  )\   )\ _   (_))   )\ /(_)|_))((_)()\ )(_)|()\ /((_) 
((/ __|((_) ((_) |  / __| ((_|_) _| |__(()((_|(_)_ ((_|_))   
 | (__/ _ \/ _ \ |  \__ \/ _ \|  _|  _\ V  V / _`+"`"+` | '_/ -_)  
  \___\___/\___/_|  |___/\___/|_|  \__|\_/\_/\__,_|_| \___|  

`;

func main() {
    fmt.Print(TITLE);
    reader := bufio.NewReader(os.Stdin);

    fmt.Print("Username: ");
    user, _ := reader.ReadString('\n');
    user = strings.TrimSpace(user);
    // Why not
    user += "I know you wanted me to stay\\But I can't ignore the crazy visions of me in LA\\And I heard that there's a special place\\Where boys and girls can all be queens every single day";

    fmt.Print("License Key: ");
    key, _ := reader.ReadString('\n');
    key = strings.TrimSpace(key);

    hash := sha256.Sum256([]byte(user));
    L := len(hash);
    for idx := range L { hash[idx] = (hash[idx] % 26) + 65; }

    a := string(hash[  : 8]);
    b := string(hash[ 8:16]);
    c := string(hash[16:24]);
    d := string(hash[24:32]);
    hash_key := strings.Join([]string{a, b, c, d}, "-");
    if hash_key == key {
        fmt.Println("Yay! Did you know that the Tyrannosaurus rex lived closer in time to us than to Stegosaurus?");
    } else {
        fmt.Println("Bad license key!");
    }
}
