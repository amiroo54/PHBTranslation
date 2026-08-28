جدول {{Armor}} {{Armor}}‌های اصلی بازی را لیست می‌کند. این جدول شامل هزینه و وزن آن‌ها و همچنین جزئیات زیر می‌باشد:

- **دسته‌بندی.** هر نوع {{Armor}} در یک دسته‌بندی قرار می‌گیرد: {{Light(Property)}}، {{Medium(Property)}}، {{Heavy}}. دسته‌بندی مشخص می‌کند برای درآوردن یا پوشیدن {{Armor}} چقدر زمان نیاز است (طبق جدول). 
- **{{ArmorClass}} ({{AC}}).** ستون {{ArmorClass}} در جدول نشان‌دهنده {{BaseAC}} وقتی آن نوع {{Armor}} را می‌پوشی نشان می‌دهد. برای مثال اگر {{LeatherArmor}} پوشیده باشی، {{BaseAC}} تو ۱۱ به اضافه {{DexterityModifier}}ت خواهد بود، در صورتی که {{AC}} تو با {{ChainMail}} ۱۶ است.  
- **{{Strength}}.** اگر ستون {{Strength}} در جدول برای یک نوع {{Armor}} یه {{StrengthScore}} نشان بدهد، آن {{Armor}} در صورتی که {{StrengthScore}} شخصی که آن را پوشیده از {{Score}} مشخص شده کمتر باشد، سرعت او به اندازه ۱۰ فوت کم می‌شود.
- **{{Stealth}}.** اگر جدول در ستون {{Stealth}} در ردیف یک نوع {{Armor}} «{{Disadvantage}}» نوشته باشد، کسی که آن را پوشیده برای {{AbilityCheck}}‌های {{Dexterity}} ({{Stealth}}) {{Disadvantage}} دارد.  

Armor

| {{Armor}}                                                                      | {{ArmorClass}} ({{AC}})               | {{Strength}}  | {{Stealth}}      | وزن       | هزینه    |
| ------------------------------------------------------------------------------ | ------------------------------------- | --------------- | ---------------- | --------- | -------- |
| _{{Armor}} {{Light(Property)}} (۱ دقیقه برای پوشیدن یا در آوردن)_              |                                       |               |                  |           |          |
| {{PaddedArmor}}                                                                | ۱۱ + {{DexterityModifier}}            | —             | {{Disadvantage}} | {{LB:8}}  | 5 GP     |
| {{LeatherArmor}}                                                               | ۱۱ + {{DexterityModifier}}            | —             | —                | {{LB:10}} | 10 GP    |
| {{StuddedLeatherArmor}}                                                        | ۱۲ + {{DexterityModifier}}            | —             | —                | {{LB:13}} | 45 GP    |
| _{{Armor}} {{Medium(Property)}} (۵ دقیقه برای پوشیدن و ۱ دقیقه برای در آوردن)_ |                                       |               |                  |           |          |
| {{HideArmor}}                                                                  | ۱۲ + {{DexterityModifier}} (حداکثر ۲) | —             | —                | {{LB:12}} | 10 GP    |
| {{ChainShirt}}                                                                 | ۱۳ + {{DexterityModifier}} (حداکثر ۲) | —             | —                | {{LB:20}} | 50 GP    |
| {{ScaleMail}}                                                                  | ۱۴ + {{DexterityModifier}} (حداکثر ۲) | —             | {{Disadvantage}} | {{LB:45}} | 50 GP    |
| {{Breastplate}}                                                                | ۱۴ + {{DexterityModifier}} (حداکثر ۲) | —             | —                | {{LB:20}} | 400 GP   |
| {{HalfPlateArmor}}                                                             | ۱۵ + {{DexterityModifier}} (حداکثر ۲) | —             | {{Disadvantage}} | {{LB:40}} | 750 GP   |
| _{{Armor}} {{Heavy}} (۱۰ دقیقه برای پوشیدن و ۵ دقیقه برای در آوردن)_           |                                       |               |                  |           |          |
| {{RingMail}}                                                                   | ۱۴                                    | —             | {{Disadvantage}} | {{LB:40}} | 30 GP    |
| {{ChainMail}}                                                                  | ۱۶                                    | {{Strength}} ۱۳ | {{Disadvantage}} | {{LB:55}} | 75 GP    |
| {{SplintArmor}}                                                                | ۱۷                                    | {{Strength}} ۱۵ | {{Disadvantage}} | {{LB:60}} | 200 GP   |
| {{PlateArmor}}                                                                 | ۱۸                                    | {{Strength}} ۱۶ | {{Disadvantage}} | {{LB:65}} | 1,500 GP |
| _{{Shield}} ({{Action}} {{Utilize}} برای پوشیدن و در آوردن)_                   |                                       |               |                  |           |          |
| {{Shield}}                                                                     | +۲                                    | —             | —                | {{LB:6}}  | 10 GP    |

### {{ArmorTraining}}

هر کسی می‌تواند یک {{Armor}} بپوشد یا یک {{Shield}} در دست داشته باشد، ولی فقط کسانی که با آن‌ها تمرین کرده باشند می‌توانند به صورت موثر از آن استفاده کنند. {{Class}} و {{Feature}}‌های دیگر هر {{Character}} {{ArmorTraining}} او را مشخص می‌کنند. هر {{Monster}} با هر {{Armor}}ی که در {{StatBlock}}ش باشد {{Training}} دارد.

#### {{Armor}} {{Light(Property)}}، {{Medium(Property)}} یا {{Heavy}}

اگر {{Armor}} {{Light(Property)}}، {{Medium(Property)}} یا {{Heavy}} پوشیده باشی و با آن {{Training}} نداشته باشی، در هر {{D20Test}}ی که شامل {{Strength}} یا {{Dexterity}} می‌شود {{Disadvantage}} داری و نمی‌توانی از {{Spell}} استفاده کنی.

#### {{Shield}}

فقط در صورتی که با {{Shield}} {{Training}} داشته باشی از افزایش {{ArmorClass}} آن بهره‌مند می‌شوی.

### فقط یکی همزمان

هر {{Creature}}ی فقط می‌تواند یک دست {{Armor}} و یک {{Shield}} همزمان بپوشد.

> #### قانون جایگزین: اندازه {{Equipment}}
> 
> در اکثر {{Campaign}}‌ها می‌توانی در چارچوب عقل سلیم از هر {{Equipment}}ی که پیدا می‌کنی استفاده کنی. برای مثال یک {{Orc}} طبیعتا در {{LeatherArmor}} یک {{Halfling}} جا نمی‌شود، و ردای یک غول برای یک {{Gnome}} بزرگ خواهد بود. 
> 
> {{DM}} می‌تواند واقع‌گرایانه‌تر عمل کند. برای مثال یک {{PlateArmor}} که برای یک انسان ساخته شده ممکن است بدون تغییر اندازه یک انسان دیگر نشود، و لباس فرم یک نگهبان ممکن است به تن کسی که می‌خواهد آن را به عنوان لباس مبدل بپوشد زار بزند.
> 
> اگر از این قانون استفاده می‌کنی، وقتی {{Adventurer}}‌ها {{Armor}}، لباس یا چیزهای مشابه برای پوشیدن پیدا می‌کنند، ممکن است نیاز داشته باشند تا به یک آهنگر، خیاط، چرم‌کار یا مختصص مشابهی مراجعه کند تا آن را قابل پوشیدن کند. خرج این کار به اندازه {{D:۱:۴}} × ۱۰ درصد قیمت آن در بازار است.