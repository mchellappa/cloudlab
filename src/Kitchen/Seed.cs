using Kitchen.Api.Models;

namespace Kitchen.Api.Data
{
    public static class Seed
    {
        public static Cupcake Chocolate = new Cupcake
        {
            Id = 1,
            Name = "Chocolate",
            Description = "Chocolatey and delicious",
            Price = 4.95m,
            Image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRgsnbhtyxwu83esiCshNY7-YCypRKUHikL58EuaX-DUq-A698-FA"
        };

        public static Cupcake Vanilla = new Cupcake
        {
            Id = 2,
            Name = "Vanilla",
            Description = "Plain, boring vanilla cupcake",
            Price = 4.95m,
            Image = "https://www.lifeloveandsugar.com/wp-content/uploads/2017/01/Moist-Vanilla-Cupcakes2.jpg"
        };

        public static Cupcake RedVelvet = new Cupcake
        {
            Id = 3,
            Name = "Red Velvet",
            Description = "Is it chocolate? I don't know! It looks red and tastes delicious",
            Price = 5.5m,
            Image = "https://therecipecritic.com/wp-content/uploads/2017/01/RedVelvetCupcakes2-667x1000.jpg"

        };

        public static Cupcake PumpkinSpice = new Cupcake
        {
            Id = 4,
            Name = "Pumpkin Spice",
            Description = "Seasonal classic that tastes like everyone's favorite squash",
            Price = 6.99m,
            Image = "https://cdn.crownmediadev.com/4a/1e/9808ba9b4487a12d0ccccc84f61c/home-family-pumpkin-spice-latte-cupcakes.jpg"

        };

        public static Cupcake Bubblegum = new Cupcake
        {
            Id = 5,
            Name = "Bubblegum",
            Description = "You asked, we delivered! Bubblegum cupcake that defies every culinary and natural rule",
            Price = 20,
            Image = "https://www.sbs.com.au/food/sites/sbs.com.au.food/files/bubblepop-electric-cupcakes_lc.jpg"

        };

        public static Cupcake Unicorn = new Cupcake
        {
            Id = 6,
            Name = "Unicorn",
            Description = "Magical and delicious! Limited edition treat made with real unicorn!",
            Price = 999.99m,
            Image = "https://media2.s-nbcnews.com/j/newscms/2018_16/1332898/unicorn-cupcakes-today-041918-tease_607876a763a32491c1bf4bb7c8eab53e.today-inline-large.jpg"
        };
    }
}
