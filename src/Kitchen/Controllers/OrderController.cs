using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Kitchen.Services;
using Microsoft.AspNetCore.Mvc;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace Kitchen.Controllers
{
    [Route("api/[controller]")]
    public class OrderController : Controller
    {
        private readonly IRepository _repository;

        public OrderController(IRepository repository)
        {
            _repository = repository;
            object foo = "bar";
            _repository.Add(foo);


        }
        // GET: api/<controller>
        [HttpGet]
        public object Get()
        {
            return _repository.Get();
        }

        // POST api/<controller>
        [HttpPost]
        public bool Post([FromBody]object model)
        {
            try
            {
                _repository.Add(model);
                return true;
            }
            catch
            {
                return false;
            }
        }

    }
}
