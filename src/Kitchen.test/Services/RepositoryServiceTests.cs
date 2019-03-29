using Kitchen.Services;
using System;
using System.Collections.Generic;
using System.Text;
using Xunit;

namespace Kitchen.test.Services
{
    public class RepositoryServiceTests
    {
        [Fact]
        public void Add_inserts_model_into_repository()
        {
            Repository repository = new Repository();

            object foo = "bar";

            repository.Add(foo);

            var onlyData = Assert.Single(repository.Data);
            Assert.Equal(foo, onlyData);
        }

        [Fact]
        public void Add_throws_if_model_is_null()
        {
            Repository repository = new Repository();

            object foo = null;

            Assert.Throws<ArgumentException>(() => repository.Add(foo));
        }
    }
}
