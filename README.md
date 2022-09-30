# Classification of emails and telephones 📖

This algorithm classifies emails and telephones by levels according to different aspects.

## Use 📝
The use is simple. Just call the function and declare the parameters. 

```
clas_emails(df,['EMAIL_1','EMAIL_2'])
```

Where *df* is the dataframe, *EMAIL_1* and *EMAIL_2* are the **columns** to be classified.

## Example 🔍
<img align="center" src=https://github.com/Cuadernin/class_tel_email/blob/main/correos.png height="240" width="350"> <br/>

A new column is created with the levels that correspond to each email. \
**In the case of telephones, it works in a similar way.**

### **Note:**
PARTE 3 and PARTE 7 contain different commented lines. This is because there are different regular expression patterns capable of detecting an email as "invalid". For example, with a regular expression __brian-95smith@yahoo.com__ is a invalid email but in others it's valid. The same thing happens with david88/_s1@company.org which in some cases is invalid and in others valid. It could even depend on the domain as well. That's why I put two more expressions, to show how it identifies one email as invalido and other doesn't.
