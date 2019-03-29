using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Kitchen.Services
{
    public interface IRepository
    {

        void Add(object model);

        object Get();
    }

    public class Repository : IRepository
    {
        public IList<object> Data = new List<object>();

        public void Add(object model)
        {
            if (model == null)
            {
                throw new ArgumentException("Model cannot be null", nameof(model));
            }

            Data.Add(model);
        }

        public object Get()
        {
            return Data.Last();
        }
    }
}
