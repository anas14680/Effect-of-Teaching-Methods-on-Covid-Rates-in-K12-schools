# Estimating the Effect of Learning Modes in K-12 Schools on COVID Positivity Rates 
## Final Project for IDS 701: Unifying Data Science <img width=90 align="right" src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Duke_University_logo.svg/1024px-Duke_University_logo.svg.png">

*Contributors: Mohammad Anas, Ying Feng, Vicky Nomwesigwa, Deekshita Saikia*

## Abstract
The Covid-19 pandemic resulted in a global crisis that impeded everyday lives. As a result, several governments thought it best to set up measures to combat its spread, including closing all schools for several weeks or months. While some schools found other ways of continuing to provide education through a mix of online, and hybrid (in-person and remote) learning, others were affected so much that they had to close (Johnson, 2021). As a result, the CDC advised implementing various mitigation measures on schools' operations, especially in communities with increased prevalence of Covid-19 rates. Since schools operating in in-person modes would affect how Covid-19 positivity rates change in the community, our research interest is to investigate the causal effect of K-12 schools’ different teaching methods on Covid-19 positivity rates in various counties in the U.S.

## Data
The datasets used in this research were obtained from MCH Strategic Data (Data, 2022) and The New York Times (Times, 2022). MCH Strategic Data included information for K-12 schools within different school districts in the U.S. with varying methods of teaching and masking policies. This dataset is available for four terms (Fall 2020-2021, Spring 2020-2021, Fall 2021- 2022, Spring 2021-2022) for each school district, and had information on student enrollments. Information on Covid-19 positive cases from each county was obtained from The New York Times,
which records Covid-19 cases within all counties since the beginning of the pandemic in the U.S. To account for the population within each county, we obtained the population information for 2020 from the United States Census Bureau (Bureau, 2022 ).

## Conclusion
From our model, we can conclude that adopting in-person teaching modes during the pandemic led to a rise in Covid-19 positivity rates. This effect was significant if the teaching mode was in-person or hybrid compared to remote teaching. However, the increase in the Covid-19 positivity rates caused by in-person teaching modes was insignificant compared to the causal effect of hybrid teaching modes. Our results align with the recent studies on Covid-19, which suggest that children can also spread the infection, especially for later variants.

## Presentation
The link to the presentation can be found [here](https://youtu.be/TegLq54Ynhk).

## References
1. Ajelli, M. L.-H. (2019). Reactive school closure weakens the network of social interactions and reduces the spread of influenza. The Proceedings of the National Academy of Sciences, 116(27), 13174-13181.
2. Bureau, U. S. (2022 , April 7). Index of /programs-surveys/popest/tables/2020- 2021/counties/totals. (n.d.). Retrieved from https://www2.census.gov/programs-surveys/popest/tables/2020-2021/counties/totals/
3. Data, M. S. (2022, April 4). COVID-19 IMPACT: School District Operation Status. Retrieved from https://www.mchdata.com/covid19/schoolclosings
4. Esposito, S. C. (2021). Comprehensive and safe school strategy during COVID-19 pandemic. Ital J Pediatr, 47(6).
5. Frey, S. H. (2021). Effects of COVID-19-Related School Closures on Student Achievement-A Systematic Review. Frontiers in Psychology, 12.
6. Johnson, C. S. (2021). Impact of Covid-19 on Educational Change: Back to School. Springer.
7. Prevention, C. f. (n.d.). Centers for Disease Control and Prevention. Guidance for COVID-19 Prevention in K-12 Schools. Retrieved April 07, 2022, from https://www.cdc.gov/coronavirus/2019-ncov/community/schools-childcare/k-12-guidance.html
8. Prevention, C. f. (n.d.). Overview of Testing for SARS-CoV-2, the virus that causes COVID-19. Retrieved April 07, 2022, from https://www.cdc.gov/coronavirus/2019-ncov/hcp/testing-overview.html?CDC_AA_refVal=https%3A%2F%2Fwww.cdc.gov%2Fcoronavirus%2F2019
9. ncov%2Fphp%2Ftesting%2Fexpanded-screening-testing.html
10. Simplemaps. (2022, April 7). Database, United States Cities. Retrieved from simplemaps: https://simplemaps.com/data/us-cities
11. Times, N. Y. (2022, April 4). Github Repository. Retrieved from https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv
12. Verhagen, P. E. (2021). Learning loss due to school closures during the COVID-19 pandemic. PNAS, 118(17).
