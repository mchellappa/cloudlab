# Test Driven Development

> The best time to plant a tree was 20 years ago. The second best time is now.

## Setup

Run the following command to create an XUnit project

```powershell
dotnet new xunit -o Kitchen.Test
dotnet new web -o Kitchen.Api

cd Kitchen.Test
dotnet add reference ../Kitchen.Api
```

Create a `nuget.config` file in both the `Kitchen.Test` and `Kitchen.Api` directories and add the following configuration:

```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
 <packageSources>
    <clear/>
    <add key="artifactory" value="https://artifactory.platform.manulife.io/artifactory/api/nuget/nuget" />

  </packageSources>
</configuration>
```

This will force nuget to target the Manulife artifactory environment when restoring packages.

## First Test

Replace the contents of `UnitTest1.cs` in the `Kitchen.Test` project with the following:

```csharp
using System;
using Xunit;

namespace Kitchen.Test
{
    public class UnitTest1
    {
        [Fact]
        public void Test1()
        {
            Assert.True(false);
        }
    }
}
```

Now `cd` into the `Kitchen.Test` directory and run the `dotnet test` command.

It should fail. Congrats!

## Applying TDD
### Inventory Service

Delete the `UnitTest1.cs` file and create a new folder named `Services` with a file named `InventoryServiceTests.cs` inside this it. Add the following code:

```csharp
using System;
using System.Threading.Tasks;
using Xunit;

namespace Kitchen.Test.Services
{
    public class InventoryServiceTests
    {
        [Fact]
        public async Task GetAllAsync_returns_all_cupcakes_in_inventory()
        {
            throw new NotImplementedException();   
        }
    }
}
```

Now, in the `Kitchen.Api` project create a corresponding folder named `Services` with a file named `InventoryService.cs` inside of it.

Add the following code:

```csharp
using System.Collections.Generic;
using System.Threading.Tasks;

namespace Kitchen.Api.Services
{
    public interface IInventoryService
    {
        Task<List<Cupcake>> GetAllAsync();
    }

    public class CupcakeRepository : ICupcakeRepository
    {
        public Task<List<Cupcake>> GetAllAsync()
        {
            throw new System.NotImplementedException();
        }
    }
}
```

### Cupcake

Currently, this will not build because `Cupcake` is not defined. To resolve this, create a folder named `Models` in the `Kitchen.Api` project and add a file named `Cupcake.cs` to it. Copy the following code:

```csharp
namespace Kitchen.Api.Models
{
    public class Cupcake
    {
        public int Id { get; set; }

        public string Name { get; set; }

        public string Description { get; set; }
        
        public decimal Price { get; set; }

        public string Image { get; set; }
    }
}
```

Add `using Kitchen.Api.Models` to the top of `IdentityService.cs` to resolve the Cupcake reference.

### Test Criteria

Now, update the body of the `InventoryServiceTests` with the following code:

```csharp
private IInventoryService CreateService()
{
    throw new NotImplementedException();
}

[Fact]
public async Task GetAllAsync_returns_all_cupcakes_in_inventory()
{
    new List<Cupcake>
    {
        new Cupcake { Name = "Chocolate" },
        new Cupcake { Name = "Vanilla" },
        new Cupcake { Name = "Red Velvet" },
    };

    var service = CreateService();

    var cupcakes = await service.GetAllAsync();

    Assert.Equal(3, cupcakes.Count);
    Assert.Equal("Chocolate", cupcakes[0].Name);
    Assert.Equal("Vanilla", cupcakes[1].Name);
    Assert.Equal("Red Velvet", cupcakes[2].Name);
}
```

Running `dotnet test` should now successfuly build the projects and result in a test failure. Let's make it pass!

### Cupcake Data Repository

Create a folder named `Data` under `Kitchen.Api` and add a file named `CupcakeRepository.cs` inside it. Add an interface named `ICupcakeRepository`.

```csharp
using System.Collections.Generic;
using System.Threading.Tasks;
using Kitchen.Api.Models;

namespace Kitchen.Api.Data
{
    public interface ICupcakeRepository
    {
        Task<List<Cupcake>> GetAllAsync();
    }

    public class CupcakeRepository : ICupcakeRepository
    {
        public Task<List<Cupcake>> GetAllAsync()
        {
            throw new System.NotImplementedException();
        }
    }
}
```

### Mock Data Layer

In our `InventoryServiceTests` we will want to mock out the `ICupcakeRepository` so that it returns the cupcakes we are looking for. To simplify this, install `Moq` (an open-source mocking library) by running the following command in the `Kitchen.Test` directory:

```powershell
dotnet add package Moq
```

Update the `InventoryServiceTests.cs` file so that it creates an instance of `Mock<ICupcakeRepository>` and set it up in the test to return the three expected cupcakes. Finally, verify that the mocked up method was called as expected.

```csharp
using System.Collections.Generic;
using System.Threading.Tasks;
using Kitchen.Api.Data;
using Kitchen.Api.Models;
using Kitchen.Api.Services;
using Moq;
using Xunit;

namespace Kitchen.Test.Services
{
    public class InventoryServiceTests
    {
        private readonly Mock<ICupcakeRepository> cupcakeRepositoryMock = new Mock<ICupcakeRepository>();

        private IInventoryService CreateService()
        {
            return new InventoryService();
        }

        [Fact]
        public async Task GetAllAsync_returns_all_cupcakes_in_inventory()
        {
            cupcakeRepositoryMock.Setup(m => m.GetAllAsync())
                .ReturnsAsync(new List<Cupcake>
                {
                    new Cupcake { Name = "Chocolate" },
                    new Cupcake { Name = "Vanilla" },
                    new Cupcake { Name = "Red Velvet" },
                })
                .Verifiable();

            var service = CreateService();

            var cupcakes = await service.GetAllAsync();

            Assert.Equal(3, cupcakes.Count);
            Assert.Equal("Chocolate", cupcakes[0].Name);
            Assert.Equal("Vanilla", cupcakes[1].Name);
            Assert.Equal("Red Velvet", cupcakes[2].Name);

            cupcakeRepositoryMock.Verify();
        }
    }
}
```

### Inventory Service Implementation

This test is almost complete. Add a class named `InventoryService` to `InventoryService.cs` that implements the `IInventoryService` interface. Add a constructor that accepts `ICupcakeRepository` as an argument and implement `GetAllAsync` so that it returns `_cupcakeRepository.GetAllAsync()`.

```csharp
public class InventoryService : IInventoryService
{
    private readonly ICupcakeRepository cupcakeRepository;

    public InventoryService(ICupcakeRepository cupcakeRepository)
    {
        this.cupcakeRepository = cupcakeRepository;
    }

    public Task<List<Cupcake>> GetAllAsync()
    {
        return cupcakeRepository.GetAllAsync();
    }
}
```

Finally, update the `CreateService` method in `InventoryServiceTests.cs` so that it returns a new instance of `InventoryService` with the object from the `ICupcakeRepository` mock.

```csharp
private IInventoryService CreateService()
{
    return new InventoryService(cupcakeRepositoryMock.Object);
}
```

## Building Web API

### MVC

Delete the `app.Run` statement `Kitchen.Api/Startup.cs`. Now, register MVC as a service and using it during app configuration as shown below.

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.DependencyInjection;

namespace Kitchen.Api
{
    public class Startup
    {
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddMvc();
        }

        public void Configure(IApplicationBuilder app, IHostingEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }

            app.UseMvc();
        }
    }
}
```

The app is now using MVC; however, it does not have any routes mapped. Add a folder named `Controllers` in `Kitchen.Api` and create a file named `InventoryController.cs`.

```csharp
using System.Collections.Generic;
using System.Threading.Tasks;
using Kitchen.Api.Models;
using Microsoft.AspNetCore.Mvc;

namespace Kitchen.Api.Controllers
{
    [Route("api/[controller]")]
    public class InventoryController : Controller
    {
        [HttpGet]
        public Task<List<Cupcake>> GetAllAsync()
        {
            throw new System.NotImplementedException();
        }
    }
}
```

Now, navigating to [https://localhost:5001/api/inventory](https://localhost:5001/api/inventory) will result in a thrown exception. Well done!

### Controller Test

Create a new folder named `Controllers` in `Kitchen.Test` and add a file named `InventoryControllerTests.cs`. Add the following code:

```csharp
using System.Collections.Generic;
using System.Threading.Tasks;
using Kitchen.Api.Controllers;
using Kitchen.Api.Models;
using Kitchen.Api.Services;
using Moq;
using Xunit;

namespace Kitchen.Test.Controllers
{
    public class InventoryControllerTests
    {
        private readonly Mock<IInventoryService> inventoryServiceMock = new Mock<IInventoryService>();

        private InventoryController CreateController()
        {
            return new InventoryController(inventoryServiceMock.Object);
        }

        [Fact]
        public async Task GetAllAsync_returns_all_cupcakes_in_inventory()
        {
            inventoryServiceMock.Setup(m => m.GetAllAsync())
                .ReturnsAsync(new List<Cupcake>
                {
                    new Cupcake { Name = "Chocolate" },
                    new Cupcake { Name = "Vanilla" },
                    new Cupcake { Name = "Red Velvet" },
                })
                .Verifiable();

            var controller = CreateController();

            var cupcakes = await controller.GetAllAsync();

            Assert.Equal(3, cupcakes.Count);
            Assert.Equal("Chocolate", cupcakes[0].Name);
            Assert.Equal("Vanilla", cupcakes[1].Name);
            Assert.Equal("Red Velvet", cupcakes[2].Name);

            inventoryServiceMock.Verify();
        }
    }
}
```

As you can probally tell, most of this test is boilerplate copied directly from `InventoryServiceTests.cs`. The exception here is that instead of mocking out the cupcake repository, we are mocking out `IInventoryService` itself. However, there are two important errors that will prevent this from building:

* The `Kitchen.Test` project does not reference the `Microsoft.AspNetCore.Mvc`
* The `InventoryController` does not have any constructor arguments

The first of these issues can be resolved by running the following command in `Kitchen.Test`:

```powershell
dotnet add package Microsoft.AspNetCore.Mvc
```

To resolve the second issue, update `InventoryController.cs` to have the matching constructor and to return `inventoryService.GetAllAsync()`.

```csharp
using System.Collections.Generic;
using System.Threading.Tasks;
using Kitchen.Api.Models;
using Kitchen.Api.Services;
using Microsoft.AspNetCore.Mvc;

namespace Kitchen.Api.Controllers
{
    [Route("api/[controller]")]
    public class InventoryController : Controller
    {
        private readonly IInventoryService inventoryService;

        public InventoryController(IInventoryService inventoryService)
        {
            this.inventoryService = inventoryService;
        }

        [HttpGet]
        public Task<List<Cupcake>> GetAllAsync()
        {
            return inventoryService.GetAllAsync();
        }
    }
}
```

### Register Services

Everything builds and both of the tests pass; however, we are now getting a new exception when we try to visit [https://localhost:5001/api/inventory](https://localhost:5001/api/inventory).
> Unable to resolve service for type 'Kitchen.Api.Services.IInventoryService'
An ASP.NET Core `Controller` relies on the [dependency injection container](https://docs.microsoft.com/en-us/aspnet/core/fundamentals/dependency-injection?view=aspnetcore-2.2) to resolve it's dependencies (rather than manually instantiating them and passing them as constructor arguments). We must now register our services so that they can be resolved by the DI container.

Add our two interfaces along with their implementations to the `ConfigureServices` method as shown below:

```csharp
public void ConfigureServices(IServiceCollection services)
{
    services.AddTransient<IInventoryService, InventoryService>();
    services.AddTransient<ICupcakeRepository, CupcakeRepository>();

    services.AddMvc();
}
```

### Data Persistence

Now, when the project is run, we are once again getting our favorite `NotImplementedException`. This is by design since the `CupcakeRepository` has not actually be implemented yet. You're witnessing the power of [Inversion of Control](https://en.wikipedia.org/wiki/Inversion_of_control)!

Create a file named `ApplicationDbContext.cs` under the `Kitchen.Api/Data` folder with the following content:

```csharp
using Kitchen.Api.Models;
using Microsoft.EntityFrameworkCore;

namespace Kitchen.Api.Data
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions options) : base(options)
        {
        }

        public DbSet<Cupcake> Cupcakes { get; set; }
    }
}
```

Let's register `ApplicationDbContext` in our `Startup.cs` file. Add the following code to the `ConfigureServices` method:

```csharp
services.AddDbContext<ApplicationDbContext>(options =>
{
    options.UseInMemoryDatabase(nameof(Kitchen));
});
```

This currently will not build. We must add a references to `Microsft.EntityFrameworkCore` and `Microsft.EntityFrameworkCore.InMemory` using the following commands:

```powershell
dotnet add package Microsoft.EntityFrameworkCore
dotnet add package Microsoft.EntityFrameworkCore.InMemory
```

Lastly, add the following `using` statments at the top of `Startup.cs` to import this newly installed method.

```csharp
using Microsoft.EntityFrameworkCore;
```

### Testing Data Repository

Add a new folder to `Kitchen.Test` called `Data` and create a file named `CupcakeRepositoryTests.cs`. Add the following test:

```csharp
using System;
using System.Threading.Tasks;
using Kitchen.Api.Data;
using Kitchen.Api.Models;
using Microsoft.EntityFrameworkCore;
using Xunit;

namespace Kitchen.Test.Data
{
    public class CupcakeRepositoryTests
    {
        private readonly ApplicationDbContext dbContext;

        public CupcakeRepositoryTests()
        {
            var dbContextOptions = new DbContextOptionsBuilder()
                .UseInMemoryDatabase(Guid.NewGuid().ToString())
                .Options;

            dbContext = new ApplicationDbContext(dbContextOptions);
        }

        private ICupcakeRepository CreateRepository()
        {
            return new CupcakeRepository(dbContext);
        }

        [Fact]
        public async Task GetAllAsync_returns_all_cupcakes_in_database()
        {
            dbContext.Cupcakes.AddRange(new Cupcake { Name = "Chocolate" },
                    new Cupcake { Name = "Vanilla" },
                    new Cupcake { Name = "Red Velvet" });
            dbContext.SaveChanges();

            var repository = CreateRepository();

            var cupcakes = await repository.GetAllAsync();

            Assert.Equal(3, cupcakes.Count);
            Assert.Equal("Chocolate", cupcakes[0].Name);
            Assert.Equal("Vanilla", cupcakes[1].Name);
            Assert.Equal("Red Velvet", cupcakes[2].Name);
        }
    }
}
```

At the moment, this will not build. Let's update the constructor for `CupcakeRepository` to accept the `ApplicationDbContext` as an argument and finally implement the `GetAllAsync` method. `CupcakeRepository.cs` should now match the following:

```csharp
using System.Collections.Generic;
using System.Threading.Tasks;
using Kitchen.Api.Models;
using Microsoft.EntityFrameworkCore;

namespace Kitchen.Api.Data
{
    public interface ICupcakeRepository
    {
        Task<List<Cupcake>> GetAllAsync();
    }

    public class CupcakeRepository : ICupcakeRepository
    {
        private readonly ApplicationDbContext dbContext;

        public CupcakeRepository(ApplicationDbContext dbContext)
        {
            this.dbContext = dbContext;
        }

        public Task<List<Cupcake>> GetAllAsync()
        {
            return dbContext.Cupcakes.ToListAsync();
        }
    }
}
```

### Seed Data

Now for the moment of truth. Run `dotnet run` in the `Kitchen.Api` direcory and then navigate to [https://localhost:5001/api/inventory](https://localhost:5001/api/inventory).
You should only see a blank page with a `[]` in the top left corner (in Chrome). This signifies (in our case) an empty array of cupcakes. However, this is clearly unnacceptable for a Cupcake Shop, so let's add some seed data!

Create a file named `Seed.cs` inside the `Kitchen.Api/Data` folder and paste the following code:

```csharp
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
```

Next, modify `ApplicationDbContext` to add a `protected override` method called `OnModelCreating`.

```csharp
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    modelBuilder.Entity<Cupcake>().HasData(Seed.Chocolate, Seed.Vanilla, Seed.RedVelvet, Seed.PumpkinSpice, Seed.Bubblegum, Seed.Unicorn);
}
```

There is one caveat to this method of seeding data: it typically relies on a database migration to invoke this method, but since we are using an in-memory database this will never be called. In order to force it to be called, update `ICupcakeRepository` to have the following `GetAllAsync` method:

```csharp
public async Task<List<Cupcake>> GetAllAsync()
{
    await dbContext.Database.EnsureCreatedAsync();
    return await dbContext.Cupcakes.ToListAsync();
}
```

## PCF

### Manifest

Create a file named `manifest.yml` inside the `src` folder. Add the following markup with your name instead of `{NAME}`:

```yml
---
applications:
- name: KitchenApi{NAME}
  path: ./Kitchen.Api
  buildpacks:
  - dotnet_core_buildpack
  memory: 256M
```

Now `cd` into the `src` directory (adjacent to the `manifest.yml` file) and run the following command to authenticate with PFC. You will be asked to enter your username and password in two separate prompts.

```powershell
cf login -a https://api.sys.cac.preview.pcf.manulife.com -o JHAS-CAC-DEV -s DE-PLAYAREA-CAC-DEV
```

Once you have authenticated, push the application using the following command:

```powershell
cf push
```

### Configure Real Database

Install Cloud Foundry Actuators

```powershell
dotnet add package Steeltoe.Management.CloudFoundryCore

dotnet add package Steeltoe.Extensions.Configuration.CloudFoundryCore
```

Install Steeltoe Database Service Connectors

```powershell
dotnet add package Steeltoe.CloudFoundry.Connector.EFCore

dotnet add package Pomelo.EntityFrameworkCore.MySql
```
